"""
Endpoints for the poly API.
"""
import json
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.config import SessionLocal
from app.models import Poly
from app.serializers import PolySerializer
from app.services.file_management import (save_matplot_figure,
                                          save_nparray_to_file)
from app.services.filling_service import fill_polyline

# Create a new router
router = APIRouter()
db = SessionLocal()


@router.get(
    "/polys", response_model=List[PolySerializer], status_code=status.HTTP_200_OK
)
def get_all_polys():
    """
    Retrieve all poly items.
    """
    polys = db.query(Poly).all()

    return polys


@router.get(
    "/polys/{poly_id}", response_model=PolySerializer, status_code=status.HTTP_200_OK
)
def get_poly_details(poly_id: int):
    """
    Retrieve details related to poly item.

    param int poly_id: The id of the poly item.
    return Poly poly: The poly item.
    """
    poly = db.query(Poly).filter(Poly.id == poly_id).first()

    if poly is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Poly not found"
        )
    return poly


@router.delete("/polys/{poly_id}")
def delete_poly(poly_id: int):
    """
    Delete a poly item.
    """
    poly_to_delete = db.query(Poly).filter(Poly.id == poly_id).first()

    if poly_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found."
        )

    db.delete(poly_to_delete)
    db.commit()

    return JSONResponse({"message": "Item deleted."}, status_code=status.HTTP_200_OK)


@router.post("/polys", status_code=status.HTTP_201_CREATED)
def create_poly(poly: PolySerializer):
    """
    Create filled poly item.

    params PolySerializer poly: poly item to create.
    return PolySerializer: The created poly item.
    """
    # check array is valid
    if not isinstance(poly.npinput, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input array must be a string",
        )

    # check db duplicates
    poly_check = db.query(Poly).filter(Poly.name == poly.name).first()
    if poly_check is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poly with that name already exists",
        )

    if poly.algorithm not in ["rourke", "flood", "fast"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid algorithm. Pick one of: rourke, flood, fast",
        )

    # process array
    poly_arr = json.loads(poly.npinput)
    results = fill_polyline(poly_arr, poly.algorithm)
    save_file = save_nparray_to_file(results[0], poly.name)
    save_plot = save_matplot_figure(results[0], poly.name)

    if save_file:
        new_poly = Poly(
            name=poly.name,
            npinput=poly.npinput,
            xsize=results[0].shape[0],
            ysize=results[0].shape[1],
            imagefile=str(save_file),
            arrayfile=str(save_plot),
            exectime=results[1],
            algorithm=poly.algorithm,
        )
        db.add(new_poly)
        db.commit()

        return JSONResponse(
            {
                "message": "Poly item created successfully.",
                "file_url": str(save_file),
                "plot_url": str(save_file),
                "execution_speed": f"{str(results[1])} seconds",
                "algorithm": poly.algorithm,
            },
            status_code=status.HTTP_201_CREATED,
        )
    return HTTPException(
        {"message": "Something went wrong creating the poly item. Please try again."},
        status_code=status.HTTP_400_BAD_REQUEST,
    )
