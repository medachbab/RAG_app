terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

# Create a web server
resource "digitalocean_droplet" "app" {
  name   = "chatbot-droplet"
  region = "fra1"
  size   = "s-1vcpu-1gb"
  image  = "ubuntu-22-04-x64"
  ssh_keys = [var.ssh_fingerprint]
}