//*------------------------------------------------------------*
// RENDER ALL CHARTS
//*------------------------------------------------------------*
export function renderAllCharts(data) {
  const { latest_month, daily_points, weekly_data, annual_points } = data;

  const monthMap = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
  };

  const annualData = annual_points.map(d => ({
    month: monthMap[d.month],
    points: d.points
  }));

  renderDonutChart("#donut-chart", daily_points);
  renderWeeklyChart(weekly_data);

  fetch(`/ecopoints/bubble-data/${latest_month}/`)
    .then(res => res.json())
    .then(data => {
      if (data.bubble_data?.length > 0) {
        renderBubbleAndBarCharts(data.bubble_data, annualData);
      } else {
        document.getElementById("bubble-plot").innerHTML = "<p>No data available for this month.</p>";
      }
    })
    .catch(err => {
      console.error("Bubble chart fetch error:", err);
      document.getElementById("bubble-plot").innerHTML = "<p>Error loading chart.</p>";
    });
}


//*------------------------------------------------------------*
// BACKGROUND & FONT COLOURS
//*------------------------------------------------------------*
export function getThemeStyles() {
  const body = document.body;
  const theme = body.getAttribute("data-bs-theme");
  return {
    background: theme === "dark" ? "#212529" : "#ffffff",
    textColor: theme === "dark" ? "#ffffff" : "#000000"
  };
}


//*------------------------------------------------------------*
// BUBBLE PLOT & HISTOGRAM (VERTICALLY STACKED)
//*------------------------------------------------------------*
export function renderBubbleAndBarCharts(bubbleData, annualPointsData) {
  const themeStyles = getThemeStyles();

  const bubblePlot = {
    "width": 700,
    "height": 300,
    "background": "transparent",
    "data": { "values": bubbleData },
    "mark": "circle",
    "encoding": {
      "x": {
        "field": "day",
        "type": "ordinal",
        "axis": {
          "title": "Day of the Month",
          "labelColor": themeStyles.textColor,
          "titleColor": themeStyles.textColor
        }
      },
      "y": {
        "field": "category",
        "type": "nominal",
        "axis": {
          "title": "Category",
          "labelColor": themeStyles.textColor,
          "titleColor": themeStyles.textColor
        }
      },
      "size": {
        "field": "points",
        "type": "quantitative",
        "scale": {"range": [20, 500]},
        "legend": null
      },
      "color": {
        "field": "category",
        "type": "nominal",
        "scale": { "scheme": "category20" },
        "legend": {
          "title": null,
          "labelExpr": "''",
          "symbolSize": 0
        }
      },
      "tooltip": [
        { "field": "day", "type": "ordinal", "title": "Day" },
        { "field": "category", "type": "nominal", "title": "Category" },
        { "field": "points", "type": "quantitative", "title": "Total ecopoints" }
      ]
    }
  };

  const annualHistogram = {
    "width": 700,
    "height": 150,
    "background": "transparent",
    "data": { "values": annualPointsData },
    "mark": "bar",
    "encoding": {
      "x": {
        "field": "points",
        "type": "quantitative",
        "axis": {
          "title": "ecopoints",
          "labelColor": themeStyles.textColor,
          "titleColor": themeStyles.textColor
        }
      },
      "y": {
        "field": "month",
        "type": "ordinal",
        "sort": [
          "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"
        ],
        "axis": {
          "title": "Month",
          "labelColor": themeStyles.textColor,
          "titleColor": themeStyles.textColor
        }
      },
      "color": {
        "field": "month",
        "type": "nominal",
        "legend": {
          "title": null,
          "labelExpr": "''",
          "symbolSize": 0
        }
      },
      "tooltip": [
        { "field": "month", "type": "ordinal", "title": "Month" },
        { "field": "points", "type": "quantitative", "title": "Total ecopoints" }
      ]
    }
  };

  const combinedSpec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "vconcat": [bubblePlot, annualHistogram],
    "spacing": 50,
    "config": {
      "background": "transparent",
      "title": { "color": themeStyles.textColor }
    }
  };

  vegaEmbed("#bubble-plot", combinedSpec, { actions: false });
}


//*------------------------------------------------------------*
// DONUT CHART
//*------------------------------------------------------------*
export function renderDonutChart(targetId, dailyPoints, goal = 50) {
  const remaining = Math.max(goal - dailyPoints, 0);

  const donutSpec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 250,
    "height": 250,
    "background": "transparent",
    "description": "Daily points donut chart",
    "data": {
      "values": [
        { "label": "ecopoints earned", "value": dailyPoints },
        { "label": "ecopoints remaining", "value": remaining }
      ]
    },
    "mark": {
      "type": "arc",
      "innerRadius": 45,
      "stroke": "#4CAF50",
      "strokeWidth": 2
    },
    "encoding": {
      "theta": { "field": "value", "type": "quantitative" },
      "color": {
        "field": "label",
        "type": "nominal",
        "scale": {
          "domain": ["ecopoints earned", "ecopoints remaining"],
          "range": ["#4CAF50", "transparent"]
        },
        "legend": null
      },
      "tooltip": [
        { "field": "label", "type": "nominal" },
        { "field": "value", "type": "quantitative" }
      ]
    },
    "view": { "stroke": "transparent" }
  };

  vegaEmbed(targetId, donutSpec, { actions: false });
}


//*------------------------------------------------------------*
// LINE AREA CHART
//*------------------------------------------------------------*
export function renderWeeklyChart(weeklyData) {
  const themeStyles = getThemeStyles();

  const dayMap = {
    2: "Mon", 3: "Tue", 4: "Wed", 5: "Thu", 6: "Fri", 7: "Sat", 1: "Sun"
  };

  const weeklyValues = weeklyData.map(d => ({
    day: dayMap[d.day],
    points: d.points
  }));

  const allDays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const weeklyValuesMap = Object.fromEntries(weeklyValues.map(d => [d.day, d.points]));
  const fullWeeklyValues = allDays.map(day => ({
    day,
    points: weeklyValuesMap[day] || 0
  }));

  const weeklySpec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 250,
    "height": 200,
    "background": "transparent",
    "data": { "values": fullWeeklyValues },
    "mark": {
      "type": "area",
      "line": true,
      "point": true,
      "interpolate": "monotone"
    },
    "encoding": {
      "x": {
        "field": "day",
        "type": "nominal",
        "sort": allDays,
        "axis": {
          "title": "Day",
          "labelColor": themeStyles.textColor,
          "titleColor": themeStyles.textColor
        }
      },
      "y": {
        "field": "points",
        "type": "quantitative",
        "axis": {
          "title": "ecopoints",
          "labelColor": themeStyles.textColor,
          "titleColor": themeStyles.textColor
        }
      },
      "tooltip": [
        { "field": "day", "type": "nominal" },
        { "field": "points", "type": "quantitative" }
      ]
    }
  };

  vegaEmbed("#weekly-graph", weeklySpec, { actions: false });
}


//*------------------------------------------------------------*
// MAIN CHART LOGIC
//*------------------------------------------------------------*
document.addEventListener("DOMContentLoaded", () => {
  const { latest_month, daily_points, weekly_data, annual_points } = window.ecopointsData;

  const monthMap = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
  };

  const annualData = annual_points.map(d => ({
    month: monthMap[d.month],
    points: d.points
  }));

  renderDonutChart("#donut-chart", daily_points);
  renderWeeklyChart(weekly_data);

  fetch(`/ecopoints/bubble-data/${latest_month}/`)
    .then(res => res.json())
    .then(data => {
      if (data.bubble_data?.length > 0) {
        renderBubbleAndBarCharts(data.bubble_data, annualData);
      } else {
        document.getElementById("bubble-plot").innerHTML = "<p>No data available for this month.</p>";
      }
    })
    .catch(console.error);
});
