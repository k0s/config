# source it

export_var() {
    if [[ "$#" != "2" ]]
    then
        echo "Must be called with two arguments"
        return 1
    fi
    # https://serverfault.com/questions/7503/how-to-determine-if-a-bash-variable-is-empty/382740#382740
    local KEY=$1
    local VALUE="${!KEY}"
    if [[ -n "${!KEY+set}" ]];
    then
        _OLD_VARS+=( "${KEY}" )
        _OLD_VALS+=( "${VALUE}" )
    else
        _OLD_UNSET+=( "${KEY}" )
    fi
    export "${1}=${2}"
}

export_var BROWSER firefox

deactivate() {
    local index=0
    for key in "${_OLD_VARS[@]}"
    do
        local value="${_OLD_VALS[$index]}"
        export "$key=$value"
        index=$((index+1))
    done
    for var in "${_OLD_UNSET[@]}"
    do
        unset "${var}"
    done
    unset deactivate
}
