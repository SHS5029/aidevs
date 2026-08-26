if [[ -z ${PROJECT_USER_ZSHRC_SOURCED:-} ]]; then
  export PROJECT_USER_ZSHRC_SOURCED=1
  [[ -r "$HOME/.zshrc" ]] && source "$HOME/.zshrc"
fi
[[ -r "$PROJECT_ROOT/.vscode/project-venv.zsh" ]] && source "$PROJECT_ROOT/.vscode/project-venv.zsh"
