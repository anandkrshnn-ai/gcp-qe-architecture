resource "google_monitoring_dashboard" "qe_dashboard" {
  dashboard_json = jsonencode({
    displayName = "GCP QE Observability Dashboard"
    gridLayout = {
      columns = "2"
      widgets = [
        {
          title = "GKE Container Error Rate"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"kubernetes.io/container/error_count\" resource.type=\"k8s_container\""
                }
              }
            }]
          }
        },
        {
          title = "Cloud Run Request Latency"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"run.googleapis.com/request_latencies\" resource.type=\"cloud_run_revision\""
                }
              }
            }]
          }
        }
      ]
    }
  })
}
