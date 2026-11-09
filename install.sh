#!/usr/bin/env bash
# run on the new Mac from inside ~/dotfiles
set -euo pipefail
DOT="$(cd "$(dirname "$0")" && pwd)"
STAMP=$(date +%Y%m%d-%H%M%S)

link() {  # link <source in repo> <target>, backing up anything real that's in the way
  local src="$DOT/$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then mv "$dst" "$dst.pre-dotfiles-$STAMP"; fi
  ln -sfn "$src" "$dst"
  echo "  $dst -> $1"
}

echo "== homebrew"
if ! command -v brew >/dev/null && [ ! -x /opt/homebrew/bin/brew ]; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
eval "$(/opt/homebrew/bin/brew shellenv)"
export PATH="/opt/homebrew/opt/node@24/bin:$PATH"   # the Brewfile npm lines need it

for t in hashicorp/tap terraform-linters/tap; do   # brew 7 refuses third-party taps until trusted
  brew tap "$t" && brew trust "$t"
done

echo "== brew bundle (mas apps need you signed into the App Store first)"
brew bundle --file="$DOT/Brewfile" || echo "!! some bundle entries failed, rerun later with: brew bundle --file=$DOT/Brewfile"

echo "== oh-my-zsh + plugins"
[ -d "$HOME/.oh-my-zsh" ] || RUNZSH=no CHSH=no KEEP_ZSHRC=yes \
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
P="$HOME/.oh-my-zsh/custom/plugins"
[ -d "$P/zsh-autosuggestions" ] || git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions "$P/zsh-autosuggestions"
[ -d "$P/zsh-syntax-highlighting" ] || git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting "$P/zsh-syntax-highlighting"

echo "== dotfiles"
for f in .zshrc .zprofile .tmux.conf .gitconfig .gitconfig-personal .gitignore_global; do
  link "home/$f" "$HOME/$f"
done
link config/starship.toml         "$HOME/.config/starship.toml"
link config/ghostty/config        "$HOME/.config/ghostty/config"

echo "== grok cli"
command -v grok >/dev/null || [ -x "$HOME/.grok/bin/grok" ] || curl -fsSL https://x.ai/cli/install.sh | bash

echo "== bernard: one persona, every agent"
link bernard/BERNARD.md "$HOME/.claude/CLAUDE.md"
link bernard/BERNARD.md "$HOME/.codex/AGENTS.md"
link bernard/BERNARD.md "$HOME/.gemini/GEMINI.md"   # antigravity + gemini cli
link bernard/BERNARD.md "$HOME/.grok/AGENTS.md"
# cursor rules need frontmatter, so this one is generated. rerun after editing BERNARD.md
mkdir -p "$HOME/.cursor/rules"
{ printf -- '---\ndescription: Bernard persona\nalwaysApply: true\n---\n\n'; cat "$DOT/bernard/BERNARD.md"; } > "$HOME/.cursor/rules/bernard.mdc"
pbcopy < "$DOT/bernard/BERNARD.md"
echo "  cursor: persona is on your clipboard, paste it into Settings > Rules > User Rules"
link claude/claude-powerline.json "$HOME/.claude/claude-powerline.json"
[ -f "$HOME/.claude/settings.json" ] || cp "$DOT/claude/settings.json" "$HOME/.claude/settings.json"

echo "== yarn (pnpm comes from the Brewfile)"
npm install -g yarn

echo "== macOS bits you had changed"
defaults write com.apple.finder AppleShowAllFiles -bool true
defaults write com.apple.dock tilesize -int 42
killall Finder Dock 2>/dev/null || true


echo
echo "done. still manual: ssh keys and gh auth login, see README.md"
