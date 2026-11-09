eval "$(/opt/homebrew/bin/brew shellenv)"

# node@24 is keg-only in brew, so it needs adding by hand
export PATH="/opt/homebrew/opt/node@24/bin:$HOME/.local/bin:$PATH"
export PATH="$PATH:$HOME/Library/Application Support/JetBrains/Toolbox/scripts"
