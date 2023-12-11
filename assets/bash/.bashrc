#!/bin/bash

autocomplete() {

  _dev_completion() {

    local DEV_PARTIAL_MATCH
    local INDEX
  
    if [[ $COMP_CWORD -gt 1 ]]; then
      IFS=$'\n' read -rd '' -a COMPREPLY <<<"$(compgen -o plusdirs -f -- "${COMP_WORDS[COMP_CWORD]}")"
      for ((INDEX=0; INDEX < ${#COMPREPLY[@]}; INDEX++)); do
          [ -d "${COMPREPLY[${INDEX}]}" ] && COMPREPLY[${INDEX}]="${COMPREPLY[${INDEX}]}/"
          [ -f "${COMPREPLY[${INDEX}]}" ] && COMPREPLY[${INDEX}]="${COMPREPLY[${INDEX}]} "
      done
    else
      DEV_PARTIAL_MATCH="${COMP_WORDS[1]}"
      IFS=$'\n' read -rd '' -a COMPREPLY <<<"$(
        grep -oE '^[a-zA-Z0-9_-]+:([^=]|$)' /app/assets/Makefile  | \
        grep -v '^command:'                                       | \
        grep "^${DEV_PARTIAL_MATCH}"                              | \
        sed 's/[^a-zA-Z0-9_-]*$//'
      )"
      for ((INDEX=0; INDEX < ${#COMPREPLY[@]}; INDEX++)); do
          COMPREPLY[${INDEX}]="${COMPREPLY[${INDEX}]} "
      done
    fi
  }

  complete -o nospace -F _dev_completion dev

  # shellcheck source=/dev/null
  [[ -f /usr/share/bash-completion/completions/git ]] && source /usr/share/bash-completion/completions/git

}

shell_customize() {

  # Terminal Colors
  if [[ -x /usr/bin/dircolors ]]; then
      # shellcheck disable=SC2015
      test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
      alias ls='ls --color=auto'
      alias grep='grep --color=auto'
      alias fgrep='fgrep --color=auto'
      alias egrep='egrep --color=auto'
  fi

  set -e
    # shellcheck source=/dev/null
    [[ -f /home/user/.bash_customize ]] && source /home/user/.bash_customize
    # shellcheck source=/dev/null
    [[ -f /home/user/.bash_git ]] && source /home/user/.bash_git
  set +e

  HOME_BINARY_PATH="/home/user/.local/bin/"
  PROMPT_COMMAND="git_status; $PROMPT_COMMAND"

  # shellcheck disable=SC2154
  PS1='${git_branch}${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

  if [[ "${PATH}" != *"${HOME_BINARY_PATH}"* ]]; then
    # Add the local bin to path, if it's not present from Docker Environment
    export PATH="/home/user/.local/bin/:${PATH}"
  fi

}

# shellcheck source=/dev/null
source "$(poetry env info -p)/bin/activate"

shell_customize
autocomplete

