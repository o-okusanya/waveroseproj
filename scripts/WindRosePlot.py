import logging
import os
logger = logging.getLogger(__name__)

import plotly.express as px
from scripts.Initial import Initializer, spd_labels, dir_labels



class WindPlot(Initializer):
    def buildFig(self, grouped):
        logger.info(f"Starting plot for station {self.station}")

        fig = px.bar_polar(
            grouped,
            r="count",
            theta="dir_bin",
            color="spd_bin",
            category_orders={
                "dir_bin": dir_labels,
                "spd_bin": spd_labels
            },
            color_discrete_sequence=["#AED6F1", "#2E86C1", "#1A5276", "#E67E22", "#C0392B"],
            title=f"Wind Rose — CBIBS Station {self.station}<br>"
                  f"<sup>{self.sd[:10]} to {self.ed[:10]}</sup>",
            labels={"spd_bin": "Speed (m/s)", "dir_bin": "Direction", "count": "Count"},
            template="plotly_white"
        )

        fig.update_layout(
            polar=dict(
                angularaxis=dict(direction="clockwise", rotation=90),
            ),
            legend_title_text="Wind Speed (m/s)",
            title_font_size=16,
            width=700,
            height=700,
        )
        return fig
    def save(self, fig, fname):
        output_dir = r"C:\Users\ncbof\hypoxia\windroseproj\dataOutput"
        os.makedirs(output_dir, exist_ok=True)
        fig.write_html(os.path.join(output_dir, f"{fname}.html"))
        fig.write_image(os.path.join(output_dir, f"{fname}.png"), scale=2)
        fig.write_image(os.path.join(output_dir, f"{fname}.svg"), scale=2)
        fig.show()

    def plot(self, grouped, fname):
        fig = self.buildFig(grouped)
        self.save(fig, fname)
        return fig