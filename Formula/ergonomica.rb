require 'formula'

class Ergonomica < Formula
  homepage 'https://github.com/ergonomica/ergonomica'
  url 'https://github.com/ergonomica/ergonomica.git'

  version "1.0.0"

  def install
     bin.install 'ergonomica.py'
     bin.install 'error_handler.py'
     bin.install 'parser.py'
     bin.install 'verbs'
  end
end
