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

#Luodaan VPC
#TODO ASETA ARVOT
resource "google_compute_network" "vpc_network" {
  name                    = "project-network"
  auto_create_subnetworks = "false"
}

#Luodaan VPC subnetwork
#TODO ASETA ARVOT
resource "google_compute_subnetwork" "vpc_subnetwork" {
  name          = "project-subnetwork"
  ip_cidr_range = "10.2.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.name
}

#Luodaan firewall-sääntö emailille
#TODO ASETA OIKEAT SÄÄNNÖT
resource "google_compute_firewall" "vpc_firewall" {
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

#Luodaan Firewall-sääntö ingress shh, voi olla oikeasti ihan tarpeeton mut jätin varuiksi
#TODO ASETA OIKEAT SÄÄNNÖT
resource "google_compute_firewall" "vpc_firewall" {
  name    = "project-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["project-allow-ssh"]
}

#Luodaan instanssi
#TODO ASETA ARVOT
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
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

#pubsub
resource "google_pubsub_topic" "topic" {
  name = "job-topic"
}

#Cron job joka käynnistää pubsubin
resource "google_cloud_scheduler_job" "job" {
  name        = "project-job"
  description = "This job executes every night at 00:00"
  schedule    = "0 0 * * *"

  pubsub_target {
    # topic.id is the topic's full resource name.
    topic_name = google_pubsub_topic.topic.id
    data       = base64encode("test")
  }
}