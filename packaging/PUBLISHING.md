# Publishing D2D

Three CLI channels, all fed from one PyPI package (`docs-to-dark`, command `d2d`).

## 0. Build

```bash
python -m pip install --upgrade build twine
python -m build              # -> dist/docs_to_dark-<ver>.tar.gz + .whl
python -m twine check dist/*
```

## 1. PyPI (baseline — pipx / pip)

Needs a PyPI account + API token (https://pypi.org/manage/account/token/).

```bash
python -m twine upload dist/*          # prompts for token, or use ~/.pypirc
# test first if you like:
# python -m twine upload --repository testpypi dist/*
```

Users then:
```bash
pipx install docs-to-dark    # isolated, recommended
# or: pip install docs-to-dark
d2d file.pdf
```
PDF conversion needs Poppler on the system (`brew install poppler` /
`apt install poppler-utils`). Image-only use needs nothing extra.

## 2. Homebrew (macOS + Linuxbrew)

Uses a personal *tap* — a separate GitHub repo named `homebrew-d2d`.

```bash
# one-time: create the repo, then
git clone https://github.com/ParsaBordbar/homebrew-d2d
mkdir -p homebrew-d2d/Formula
cp packaging/homebrew/d2d.rb homebrew-d2d/Formula/d2d.rb
```

Edit `Formula/d2d.rb`:
- set `url` to the PyPI sdist URL and `sha256` (`shasum -a 256 dist/*.tar.gz`),
- generate dependency resources: `brew update-python-resources Formula/d2d.rb`,
- test locally: `brew install --build-from-source ./Formula/d2d.rb && brew test d2d`.

Commit + push. Users install with:
```bash
brew install ParsaBordbar/d2d/d2d
```

## 3. AUR (Arch Linux)

```bash
git clone ssh://aur@aur.archlinux.org/d2d.git
cp packaging/aur/PKGBUILD d2d/
cd d2d
updpkgsums                                   # fills sha256sums
makepkg --printsrcinfo > .SRCINFO
git add PKGBUILD .SRCINFO && git commit -m "d2d 2.0.0" && git push
```

Users: `yay -S d2d` (or any AUR helper).

## Release checklist per version

1. Bump `version` in `pyproject.toml`.
2. `python -m build && twine check dist/*`.
3. `twine upload dist/*`.
4. Update `url`/`sha256`/resources in the Homebrew formula, push tap.
5. Bump `pkgver`, `updpkgsums`, regen `.SRCINFO`, push AUR.
