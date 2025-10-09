# Root module intentionally minimal. Compose submodules from org/networking/data/app.
module "org" {
  source = "./org"
}
module "networking" {
  source = "./networking"
}
module "data" {
  source = "./data"
}
module "app" {
  source = "./app"
}
