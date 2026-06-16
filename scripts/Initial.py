import numpy as np
import pandas as pd
import logging
logger = logging.getLogger(__name__)
from cfg.apiconfig import WaveAPIConfig

dir_bins = np.arange(0, 361, 45)
dir_labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
hgt_bins = [0, 0.5, 1, 2, 4]
hgt_labels = ["0-.5", ".5-1", "1-2", "2-4"]

class Initializer(WaveAPIConfig):
    def setupParameters(self, station, sd, ed):
        self.base = "https://mw.buoybay.noaa.gov/api/v1"
        self.key = "f159959c117f473477edbdf3245cc2a4831ac61f"
        self.station = station
        self.sd = sd
        self.ed = ed
        logger.info(f"Parameters set for station {self.station} ({self.sd} to {self.ed})")
        return self

    def getData(self):
        logger.info(f"Fetching data for station {self.station}")
        height = self.fetch_var("sea_surface_wave_significant_height")
        direction = self.fetch_var("sea_surface_wave_from_direction")

        height = height.rename(columns={"value": "wave_height"})
        direction = direction.rename(columns={"value": "wave_dir"})

        logger.debug(f"Height shape: {height.shape}, Direction shape: {direction.shape}")

        wave = (
            height
            .merge(direction, on="time")
        )[["time", "wave_height", "wave_dir"]]
        logger.debug(f"Merged wave shape: {wave.shape}")
        return wave

    def Bins(self, wave):
        wave["dir_bin"] = pd.cut(
            wave["wave_dir"],
            bins=dir_bins,
            labels=dir_labels,
            include_lowest=True
        )

        wave["hgt_bin"] = pd.cut(
            wave["wave_height"],
            bins=hgt_bins,
            labels=hgt_labels,
            include_lowest=True
        )

        grouped = (
            wave.groupby(["dir_bin", "hgt_bin"], observed=True)
            .size()
            .reset_index(name="count")
        )
        logger.debug(f"Grouped shape: {grouped.shape}")
        return grouped



