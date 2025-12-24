variable "do_token" {
  type      = string
  sensitive = true
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key file in my local"
  type        = string
}