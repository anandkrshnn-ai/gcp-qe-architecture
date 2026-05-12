resource "google_monitoring_dashboard" "safety_dashboard" {
  project        = var.project_id
  dashboard_json = <<EOF
{
  "displayName": "${var.dashboard_name}",
  "gridLayout": {
    "columns": "2",
    "widgets": [
      {
        "title": "Agent Consensus Success Rate",
        "scorecard": {
          "sparkChartConfiguration": {
            "parameter": "MIN_TIME",
            "sparkChartType": "SPARK_CHART_TYPE_UNSPECIFIED"
          },
          "thresholds": [
            {
              "color": "YELLOW",
              "direction": "BELOW",
              "label": "Low Consensus",
              "value": 0.5
            }
          ],
          "timeSeriesQuery": {
            "timeSeriesFilter": {
              "filter": "resource.type=\"global\" AND jsonPayload.event=\"Consensus check complete.\" AND jsonPayload.quorum_reached=\"true\"",
              "aggregation": {
                "alignmentPeriod": "60s",
                "crossSeriesReducer": "REDUCE_COUNT",
                "perSeriesAligner": "ALIGN_RATE"
              }
            }
          }
        }
      },
      {
        "title": "Safety Gate Blocks",
        "xyChart": {
          "chartOptions": {
            "mode": "COLOR"
          },
          "dataSets": [
            {
              "plotType": "STACKED_BAR",
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"global\" AND jsonPayload.event=\"Operation NOT in allow-list.\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "crossSeriesReducer": "REDUCE_COUNT",
                    "perSeriesAligner": "ALIGN_COUNT"
                  }
                }
              }
            }
          ]
        }
      },
      {
        "title": "Model Armor Redactions",
        "scorecard": {
          "timeSeriesQuery": {
            "timeSeriesFilter": {
              "filter": "resource.type=\"global\" AND jsonPayload.event=\"ModelArmor: Secret pattern detected. Redacting.\"",
              "aggregation": {
                "alignmentPeriod": "60s",
                "crossSeriesReducer": "REDUCE_COUNT",
                "perSeriesAligner": "ALIGN_COUNT"
              }
            }
          }
        }
      }
    ]
  }
}
EOF
}
