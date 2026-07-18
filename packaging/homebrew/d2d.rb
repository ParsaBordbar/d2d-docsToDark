# Homebrew formula for D2D — Docs to Dark.
#
# This lives in your tap repo `ParsaBordbar/homebrew-d2d` as `Formula/d2d.rb`.
# Users then install with:  brew install ParsaBordbar/d2d/d2d
#
# BEFORE THIS WORKS you must:
#   1. Publish `docs-to-dark` to PyPI (see packaging/PUBLISHING.md).
#   2. Fill `url` + `sha256` below from the PyPI sdist.
#   3. Auto-generate the `resource` stanzas for the Python deps:
#        brew install pipgrip                     # helper
#        brew update-python-resources Formula/d2d.rb
#      (run from the tap repo; it rewrites the resource blocks in place)
class D2d < Formula
  include Language::Python::Virtualenv

  desc "Invert PDFs and images into dark mode"
  homepage "https://github.com/ParsaBordbar/d2d-docsToDark"
  # PLACEHOLDER — replace after publishing to PyPI:
  url "https://files.pythonhosted.org/packages/source/d/docs-to-dark/docs_to_dark-2.0.0.tar.gz"
  sha256 "REPLACE_WITH_SDIST_SHA256"
  license "MIT"

  depends_on "python@3.12"
  depends_on "poppler" # runtime dep for PDF rendering (pdf2image)

  # BEGIN generated resources — run `brew update-python-resources Formula/d2d.rb`
  # to populate pillow, numpy, pdf2image (+ transitive) here.
  # END generated resources

  def install
    virtualenv_install_with_resources
  end

  test do
    require "base64"
    # 1x1 white PNG
    png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    (testpath/"w.png").write(Base64.decode64(png))
    system bin/"d2d", "-t", "invert", testpath/"w.png"
    assert_predicate testpath/"w_dark.png", :exist?
  end
end
