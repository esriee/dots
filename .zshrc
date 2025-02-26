# Auto-attach to tmux session if not already in one
if command -v tmux &> /dev/null && [ -z "$TMUX" ]; then
  tmux attach-session -t default || tmux new-session -s default
fi

# Enable zsh completion system
autoload -Uz compinit
zstyle ':completion:*' menu select
zstyle ':completion::complete:*' gain-privileges 1
compinit

# Enable fast syntax highlighting
source /usr/share/zsh/plugins/fast-syntax-highlighting/fast-syntax-highlighting.plugin.zsh

# Aliases
alias ls="ls --color"
alias fff="command ls -a | fzf | xargs -I{} cat {}"
alias vim="nvim"

# VCS info for Git branch
autoload -Uz vcs_info
precmd() { vcs_info }  # Runs vcs_info before each prompt display

setopt prompt_subst
zstyle ':vcs_info:git:*' formats '%F{blue}%b%f'  # Show Git branch in blue
PROMPT='%F{green}%n%f:%F{blue}${vcs_info_msg_0_}%f:%F{magenta}%~%f> '  # Customize prompt


