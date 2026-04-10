import geopandas as gpd
from pyproj import Transformer
from flask import jsonify, Blueprint, request
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon
from flask_jwt_extended import jwt_required

bp = Blueprint('coordinates', __name__, url_prefix='/coordinates')

# Load severity data from CSV
def load_severity_data(csv_path):
    return pd.read_csv(csv_path)

severity_data = load_severity_data('../Cleaned_Dataset/severity_indicators_by_dauid.csv')
severity_dauids = severity_data['DAUID'].tolist()

def get_severity(dauid):
    dauid_str = str(dauid)

    # Ensure DAUID column in severity_data is also of type string
    severity_data['DAUID'] = severity_data['DAUID'].astype(str)

    # Perform the boolean indexing correctly
    row = severity_data[severity_data['DAUID'] == dauid_str]
    if not row.empty:
        score = row.iloc[0]['Composite_Severity_Score']

        # Ensure the score is JSON serializable
        if isinstance(score, (int, float, str)):
            return {'Composite_Severity_Score': score}
        else:
            return {'Composite_Severity_Score': str(score)}

    return {'Composite_Severity_Score': 0}

def get_center_and_polygon_coordinates(shapefile_path, dauid):
    gdf = gpd.read_file(shapefile_path)
    filtered_gdf = gdf[gdf['DAUID'] == dauid]

    if filtered_gdf.empty:
        return None, None

    geometry = filtered_gdf.geometry.iloc[0]
    centroid = geometry.centroid

    source_crs = "EPSG:3347"
    target_crs = "EPSG:4326"
    transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

    lon, lat = transformer.transform(centroid.x, centroid.y)

    polygon_coords = [transformer.transform(coord[0], coord[1]) for coord in geometry.exterior.coords]

    return (lat, lon), polygon_coords

def get_polygon_coords(geometry, transformer):
    if isinstance(geometry, Polygon):
        return [transformer.transform(coord[0], coord[1]) for coord in geometry.exterior.coords]
    elif isinstance(geometry, MultiPolygon):
        coords = []
        for polygon in geometry:
            coords.extend([transformer.transform(coord[0], coord[1]) for coord in polygon.exterior.coords])
        return coords
    return []

def get_all_das_coordinates(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    severity_dauids_str = [str(dauid) for dauid in severity_dauids]

    gdf = gdf[gdf['DAUID'].isin(severity_dauids_str)]  # Filter to include only DAUIDs in severity data
    all_das = []

    source_crs = "EPSG:3347"
    target_crs = "EPSG:4326"
    transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

    for _, row in gdf.iterrows():
        dauid = row['DAUID']
        geometry = row.geometry
        centroid = geometry.centroid
        lon, lat = transformer.transform(centroid.x, centroid.y)
        polygon_coords = get_polygon_coords(geometry, transformer)

        severity_score = get_severity(dauid)

        all_das.append({
            'DAUID': dauid,
            'center': {'lat': lat, 'lng': lon},
            'polygon_coords': [{'lat': lat, 'lng': lng} for lng, lat in polygon_coords],
            'severity_score': severity_score
        })

    return all_das

@bp.route('/get-all-das-coordinates', methods=['GET'])
@jwt_required()
def get_all_das_coordinates_route():
    shapefile_path = './lda_000b21a_e/lda_000b21a_e.shp'
    all_das = get_all_das_coordinates(shapefile_path)
    return jsonify(all_das)


@bp.route('/get-da-coordinates', methods=['GET'])
@jwt_required()
def get_da_coordinates():
    dauid = request.args.get('dauid')
    shapefile_path = './lda_000b21a_e/lda_000b21a_e.shp'

    if not dauid:
        return jsonify({"error": "DAUID is required"}), 400

    center, polygon_coords = get_center_and_polygon_coordinates(shapefile_path, dauid)
    if center is None:
        return jsonify({"error": f"No DAUID {dauid} found in the shapefile."}), 404

    return jsonify({
        "center": {"lat": center[0], "lng": center[1]},
        "polygon_coords": [{"lat": lat, "lng": lng} for lng, lat in polygon_coords]
    })