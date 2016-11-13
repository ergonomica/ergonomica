require 'formula'

class Ergo < Formula
  homepage 'https://github.com/ergonomica/ergonomica'
  url 'https://github.com/ergonomica/ergonomica.git'

  version "1.0.0"

  def install
     bin.install 'ergonomica'
     bin.install 'ergo'
     bin.install 'error_handler.py'
     bin.install 'parser.py'
     bin.install 'verbs'
     bin.install 'autocomplete'
  end
end
