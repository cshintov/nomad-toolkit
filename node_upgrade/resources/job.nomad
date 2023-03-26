variable "image" {
  default = "ealen/echo-server"
}

job "hello-world" {
  region = "europe-central"
  datacenters = ["LIM1", "LIM3", "HIL1"]

  type = "service"

  group "hello" {
    count = 2

    network {
      port "http" {
        static = 5678
        to = 80
      }
    }

    task "hello" {
      driver = "docker"
      config {
        image = var.image
      }

      resources {
        cpu = 100
        memory = 64
      }

      service {
        name = "hello-world"
        port = "http"
        tags = ["echo"]
      }
    }
  }
}

