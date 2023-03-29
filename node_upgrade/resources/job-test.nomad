variable "image" {
  default = "ealen/echo-server:0.6.0"
}

job "hello-world-test" {
  region = "europe-central"
  datacenters = ["LIM1", "LIM3", "HIL1"]

  type = "service"

  group "hello" {
    count = 3

    constraint {
      attribute = "${attr.unique.hostname}"
      operator  = "!="
      value     = "eu-de1-09"
    }

    network {
      port "http_bor" {
        static = 5678
        to = 80
      }

      port "http_heimdall" {
        static = 5679
        to = 80
      }
    }

    task "hello-bor" {
      driver = "docker"
      config {
        image = var.image
      }

      resources {
        cpu = 100
        memory = 64
      }

      service {
        name = "hello-bor"
        port = "http_bor"
        tags = ["echo"]
      }
    }

    task "hello_heimdall" {
      driver = "docker"
      config {
        image = var.image
      }

      resources {
        cpu = 100
        memory = 64
      }

      service {
        name = "hello-heimdall"
        port = "http_heimdall"
        tags = ["echo"]
      }
    }
  }

  group "hello_canary" {
    count = 1

    constraint {
      attribute = "${attr.unique.hostname}"
      operator  = "="
      value     = "eu-de1-09"
    }

    network {
      port "http_bor" {
        static = 5678
        to = 80
      }

      port "http_heimdall" {
        static = 5679
        to = 80
      }
    }

    task "hello-bor" {
      driver = "docker"
      config {
        image = var.image
      }

      resources {
        cpu = 100
        memory = 64
      }

      service {
        name = "hello-bor"
        port = "http_bor"
        tags = ["echo"]
      }
    }

    task "hello_heimdall" {
      driver = "docker"
      config {
        image = var.image
      }

      resources {
        cpu = 100
        memory = 64
      }

      service {
        name = "hello-heimdall"
        port = "http_heimdall"
        tags = ["echo"]
      }
    }
  }
}

