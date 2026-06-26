import logging
logger = logging.getLogger(__name__)
from cfg.loggingconfig import setup_logging
from datetime import datetime, timedelta, timezone
from scripts.WaveRosePlot import WavePlot
from cfg.databaseconfig import database

setup_logging()

class Pipeline24HR(WavePlot):
    def run24hr(self, stations):
        now = datetime.now(timezone.utc)
        self.ed = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.sd = (now - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

        results = {}
        for station in stations:
            logger.info(f"Running[24hr] {self.sd} -> {self.ed} for {station}")
            self.setupParameters(
                station=station,
                sd=self.sd,
                ed=self.ed,
            )
            try:
                wave = self.getData()
                if wave is None or wave.empty:
                    logger.warning(f"No data for {station}, skipping")
                    continue
                database(self, wave)
                results[station] = self.Bins(wave)
            except Exception as e:
                logger.error(f"Skipping {station}: {e}")
        if not results:
            logger.error("No stations returned data; nothing to plot")
            return

        display_title = f"24HR Wind Roses — {self.sd} to {self.ed}"
        out_name = f"wind_rose_24hr_ALL"

        fig = self.buildGrid(results, fname=display_title)
        self.save(fig, fname=out_name)

if __name__ == "__main__":
    if __name__ == "__main__":
        stations = ['AN', 'SR', 'PL', 'UP', 'GR']
        logger.info(f"Running Seasonal for {stations}")
        Pipeline24HR().run24hr(stations)