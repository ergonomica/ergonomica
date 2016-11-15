require 'formula'

class Ergo < Formula
  homepage 'https://github.com/ergonomica/ergonomica'
  url 'https://github.com/ergonomica/ergonomica.git'

  version "1.0.0"

  def install
    bin.install "ergo"
    bin.install "ergonomica"
    bin.install "lib"
  end
end
