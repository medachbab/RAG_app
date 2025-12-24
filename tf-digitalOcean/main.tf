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

# copying the public key from the local to digital ocean (from the terraform documentation)
resource "digitalocean_ssh_key" "default" {
  name       = "Terraform"
  public_key = file(var.ssh_public_key_path)
}

# Create a web server
resource "digitalocean_droplet" "app" {
  name     = "chatbot-droplet"
  region   = "fra1"
  size     = "s-1vcpu-1gb"
  image    = "ubuntu-22-04-x64"
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
}