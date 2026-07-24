# Load the user's normal interactive zsh configuration first.
_aidevs_zdotdir="$ZDOTDIR"
ZDOTDIR="$AIDEVS_USER_ZDOTDIR"
if [[ "$ZDOTDIR" != "$_aidevs_zdotdir" && -r "$ZDOTDIR/.zshrc" ]]; then
  source "$ZDOTDIR/.zshrc"
fi
ZDOTDIR="$_aidevs_zdotdir"
unset _aidevs_zdotdir

# Activate the shared aidevs virtual environment in every workspace terminal.
if [[ -r "$AIDEVS_VENV/bin/activate" ]]; then
  source "$AIDEVS_VENV/bin/activate"
else
  print -u2 -- "aidevs: virtual environment not found: $AIDEVS_VENV"
fi
