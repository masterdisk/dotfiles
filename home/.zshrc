export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME=""   # starship draws the prompt

plugins=(
  git
  docker
  kubectl
  terraform
  zsh-autosuggestions
  zsh-syntax-highlighting
)

# before oh-my-zsh so its single compinit picks these up
fpath=(~/.grok/completions/zsh $fpath)

source $ZSH/oh-my-zsh.sh

eval "$(starship init zsh)"
source <(fzf --zsh)
eval "$(zoxide init zsh)"

# ============================
# PATH (brew + node live in .zprofile)
# ============================
export BUN_INSTALL="$HOME/.bun"
path=(
  "$HOME/.grok/bin"
  "$BUN_INSTALL/bin"
  $path
  "$HOME/.lmstudio/bin"
  "$HOME/.spicetify"
)
typeset -U path
[ -s "$BUN_INSTALL/_bun" ] && source "$BUN_INSTALL/_bun"

# ============================
# Environment
# ============================
export EDITOR="cursor --wait"
export LANG=en_US.UTF-8
export NODE_OPTIONS="--no-deprecation"

# ============================
# Claude Code
# ============================
alias c="claude"
alias cc="claude --continue"
alias ccf="claude -p"

# ============================
# Navigation + modern CLI
# ============================
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias cat="bat"
alias ls="eza --icons"
alias ll="eza -la --icons"
alias la="eza -a --icons"
alias tree="eza --tree --icons"
alias find="fd"
alias grep="rg"

# ============================
# Git
# ============================
alias gs="git status"
alias gp="git push"
alias gl="git pull"
alias gco="git checkout"
alias gcm="git commit -m"
alias gaa="git add --all"
alias gd="git diff"
alias gb="git branch"
alias glog="git log --oneline --graph --decorate"

# ============================
# tmux
# ============================
alias ta="tmux attach -t"
alias tn="tmux new -s"
alias tl="tmux list-sessions"
alias tk="tmux kill-session -t"

# ============================
# Functions
# ============================

mkcd() {
  mkdir -p "$1" && cd "$1"
}

gacp() {
  git add --all
  git commit -m "$1"
  git push
}

# machine-specific extras, not in this repo
[ -f ~/.zshrc.local ] && source ~/.zshrc.local
