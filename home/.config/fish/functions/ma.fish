function ma --description 'Launch MangoWC using the NVIDIA DRM device'
    env WLR_DRM_DEVICES=/dev/dri/card1 dbus-run-session mango $argv
end
