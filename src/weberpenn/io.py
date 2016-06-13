"""
  Reader and Writer to and from arbaro xml file.
  
  Author: Christophe Pradal (christophe.pradal@cirad.fr)
"""

from tree_client import *
import xml.etree.ElementTree as xml


def read_arbaro_xml(filename):
    symbols = {}

    doc = xml.parse(filename)
    root = doc.getroot()
    if root.tag != 'arbaro':
        return
    species = root.getchildren()
    if len(species) == 0:
        return
    species = species[0]

    params = species.getchildren()
    for p in params:
        if p.tag == 'param':
            content = p.attrib
            symbols[content['name']] = content['value']

    return _arbaro2params(symbols)


def _arbaro2params(symbols):
    shape_id = int(symbols["Shape"])
    base_size = float(symbols["BaseSize"])
    scale = (float(symbols["Scale"]), float(symbols["ScaleV"]))
    order = int(symbols["Levels"])
    ratio = float(symbols["Ratio"])
    ratio_power = float(symbols["RatioPower"])
    lobes = [0, 0]
    if "Lobes" in symbols:
        lobes[0] = int(symbols["Lobes"])
    if "LobeDepth" in symbols:
        lobes[1] = float(symbols["LobeDepth"])

    flare = float(symbols["Flare"])

    leaves = int(symbols["Leaves"])
    leaf_scale = float(symbols["LeafScale"])
    leaf_scale_x = float(symbols["LeafScaleX"])
    base_split = int(symbols["0BaseSplits"])

    n_length = [(float(symbols["0Length"]), float(symbols["0LengthV"]))]
    if symbols.get("1Length"):
        n_length.append((float(symbols["1Length"]), float(symbols["1LengthV"])))
    if symbols.get("2Length"):
        n_length.append((float(symbols["2Length"]), float(symbols["2LengthV"])))
    if symbols.get("3Length"):
        n_length.append((float(symbols["3Length"]), float(symbols["3LengthV"])))
    
    n_seg_split = [0, 0, 0, 0]
    if "0SegSplits" in symbols:
        n_seg_split = [float(symbols["0SegSplits"])]
    if "1SegSplits" in symbols:
        n_seg_split.append(float(symbols["1SegSplits"]))
    if "2SegSplits" in symbols:
        n_seg_split.append(float(symbols["2SegSplits"]))
    if "3SegSplits" in symbols:
        n_seg_split.append(float(symbols["3SegSplits"]))

    n_split_angle = []
    if "0SplitAngle" in symbols:
        n_split_angle.append(
            (float(symbols["0SplitAngle"]), float(symbols["0SplitAngleV"])))
    if "1SplitAngle" in symbols:
        n_split_angle.append(
            (float(symbols["1SplitAngle"]), float(symbols["1SplitAngleV"])))
    if "2SplitAngle" in symbols:
        n_split_angle.append(
            (float(symbols["2SplitAngle"]), float(symbols["2SplitAngleV"])))
    if "3SplitAngle" in symbols:
        n_split_angle.append(
            (float(symbols["3SplitAngle"]), float(symbols["3SplitAngleV"])))

    n_down_angle = []
    if "1DownAngle" in symbols:
        n_down_angle.append(
            (float(symbols["1DownAngle"]), float(symbols["1DownAngleV"])))
    if "2DownAngle" in symbols:
        n_down_angle.append(
            (float(symbols["2DownAngle"]), float(symbols["2DownAngleV"])))
    if "3DownAngle" in symbols:
        n_down_angle.append(
            (float(symbols["3DownAngle"]), float(symbols["3DownAngleV"])))

    n_curve = [(int(symbols["0CurveRes"]), float(symbols["0Curve"]),
                float(symbols["0CurveV"]), float(symbols["0CurveBack"]))]
    if "1CurveRes" in symbols:
        n_curve.append((int(symbols["1CurveRes"]), float(symbols["1Curve"]),
                        float(symbols["1CurveV"]),
                        float(symbols["1CurveBack"])))
    if "2CurveRes" in symbols:
        n_curve.append((int(symbols["2CurveRes"]), float(symbols["2Curve"]),
                        float(symbols["2CurveV"]),
                        float(symbols["2CurveBack"])))
    if "3CurveRes" in symbols:
        n_curve.append((int(symbols["3CurveRes"]), float(symbols["3Curve"]),
                        float(symbols["3CurveV"]),
                        float(symbols["3CurveBack"])))

    n_rotate = [(float(symbols["1Rotate"]), float(symbols["1RotateV"]))]
    if "2Rotate" in symbols:
        n_rotate.append((float(symbols["2Rotate"]), float(symbols["2RotateV"])))
    if "3Rotate" in symbols:
        n_rotate.append((float(symbols["3Rotate"]), float(symbols["3RotateV"])))

    branches = [int(symbols["1Branches"])]
    if "2Branches" in symbols:
        branches.append(int(symbols["2Branches"]))
    if "3Branches" in symbols:
        branches.append(int(symbols["3Branches"]))

    while len(branches) < order:
        branches.append(branches[-1])

    n_taper = [float(symbols["0Taper"])]
    if "1Taper" in symbols:
        n_taper.append(float(symbols["1Taper"]))
    if "2Taper" in symbols:
        n_taper.append(float(symbols["2Taper"]))
    if "3Taper" in symbols:
        n_taper.append(float(symbols["3Taper"]))

    rotate = [0] * (order + 1)

    params = TreeParameter(shape_id, base_size, scale, order,
                           ratio, ratio_power, lobes, flare,
                           base_split, n_length,
                           n_seg_split, n_split_angle, n_down_angle,
                           n_curve, n_rotate, branches, leaves, leaf_scale,
                           leaf_scale_x,
                           rotate)
    params.n_taper = n_taper
    return params
