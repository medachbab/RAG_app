terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "default" {
  name = "Terraform"
}

resource "digitalocean_droplet" "app" {
  name     = "ecom-app-prod"
  region   = "fra1"
  # CHANGED: Resized to 4GB RAM to handle 7+ containers and AI services
  size     = "s-2vcpu-4gb" 
  image    = "ubuntu-22-04-x64"
  ssh_keys = [data.digitalocean_ssh_key.default.id]
}