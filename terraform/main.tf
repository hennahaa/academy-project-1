terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

#Asetetaan credentiaalit, projekti ja oletusalueet
provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

#Luodaan VPC network nimeltä project-network, luodaan sille subnet erikseen
resource "google_compute_network" "vpc_network" {
  name                    = "project-network"
  auto_create_subnetworks = "false"
}

#Luodaan project-networkille subnetwork nimeltä subnet-1
resource "google_compute_subnetwork" "vpc_subnetwork" {
  name          = "subnet-1"
  ip_cidr_range = "10.2.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.name
}

#Luodaan EGRESS firewall-sääntö emailille
resource "google_compute_firewall" "vpc_firewall_1" {
  name    = "project-email"
  network = google_compute_network.vpc_network.name

  #liikenne VM:stä ulos
  direction = "EGRESS"

  allow {
    protocol = "tcp"
    ports    = ["2525"]
  }

  target_tags = ["project-allow-email"]
}

#Luodaan INGRESS firewall-sääntö SSH:n käyttämiseen
resource "google_compute_firewall" "vpc_firewall_2" {
  name    = "project-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["project-allow-ssh"]
}

#Luodaan instanssi
resource "google_compute_instance" "vm_instance" {
  name         = "hour-instance"
  machine_type = "f1-micro"
  tags         = ["project-allow-email", "project-allow-ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.name
    subnetwork = google_compute_subnetwork.vpc_subnetwork.name
    access_config {
    }
  }
  metadata_startup_script = file("startup.sh")
}