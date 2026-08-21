import rasterio
import numpy as np
import CONFIG

def reclassify(array, breaks_and_scores):
    out = np.zeros_like(array)
    for lo, hi, score in breaks_and_scores:
        out[(array >= lo) & (array < hi)] = score
    return out


def get_percentile_edges(n_classes, flatness_rating):
    """
    flatness_rating: 1 (very flat/low-lying) to 5 (hilly)
    Flat terrain -> finer resolution near the low end (skewed percentiles)
    Hilly terrain -> more even/linear percentile spacing
    """
    if flatness_rating <= 1:
        # heavily skewed toward capturing subtle low-end variation
        percentiles = [0, 10, 25, 50, 75, 100][:n_classes+1]
    elif flatness_rating == 2:
        percentiles = [0, 15, 35, 60, 85, 100][:n_classes+1]
    elif flatness_rating == 3:
        percentiles = np.linspace(0, 100, n_classes + 1)  # standard equal split
    elif flatness_rating == 4:
        percentiles = [0, 20, 45, 70, 90, 100][:n_classes+1]
    else:  # 5, hilly
        percentiles = [0, 30, 55, 80, 95, 100][:n_classes+1]
    return percentiles


def ask_flatness_rating():
    print("How flat is your region?")
    print("  1 = low-lying / very flat land")
    print("  5 = hilly / steep terrain")
    while True:
        try:
            val = int(input("Enter a rating from 1 to 5: "))
            if 1 <= val <= 5:
                return val
        except ValueError:
            pass
        print("Please enter a whole number between 1 and 5.")


def auto_breaks_and_scores(arr, scores, flatness_rating):
    n = len(scores)
    percentiles = get_percentile_edges(n, flatness_rating)
    edges = np.nanpercentile(arr, percentiles)
    edges = np.unique(edges)

    breaks = []
    for i  in range(len(edges) - 1):
        lo = edges[i]
        hi = edges[i + 1] if i < len(edges) - 2 else edges[i + 1] + 1e-6
        breaks.append((lo, hi, scores[i]))
    return breaks


def reclassify_layer_auto(src_path, out_path, scores, flatness_rating):
    with rasterio.open(src_path) as src:
        arr = src.read(1)
        profile = src.profile

    breaks_and_scores = auto_breaks_and_scores(arr, scores, flatness_rating)
    print(f"{src_path} auto-breaks (flatness={flatness_rating}): {breaks_and_scores}")

    score = reclassify(arr, breaks_and_scores)
    profile.update(dtype=rasterio.float32)
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(score.astype(rasterio.float32), 1)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    flatness = ask_flatness_rating()

    reclassify_layer_auto(CONFIG.SLOPE_PATH, CONFIG.SLOPE_SCORE_PATH, [10,8,6,4,2], flatness)
    reclassify_layer_auto(CONFIG.FLOW_ACC_PATH, CONFIG.FLOW_SCORE_PATH, [2,5,8,10], flatness)
    reclassify_layer_auto(CONFIG.NDVI_PATH, CONFIG.NDVI_SCORE_PATH, [9,6,2], flatness)
    reclassify_layer_auto(CONFIG.SOIL_STD_PATH, CONFIG.SOIL_SCORE_PATH, [2,5,8,10], flatness)