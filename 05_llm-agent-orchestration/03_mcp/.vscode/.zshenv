if [[ -z ${PROJECT_USER_ZSHENV_SOURCED:-} ]]; then
  export PROJECT_USER_ZSHENV_SOURCED=1
  [[ -r "$HOME/.zshenv" ]] && source "$HOME/.zshenv"
fi
