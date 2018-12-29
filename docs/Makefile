PHONY: cast gif

cast:
	osascript movie.applescript
play:
	asciinema play movie.cast
gif:
	bash -c "which convert || brew install imagemagick"
	bash -c "which asciicast2gif || brew install asciicast2gif"
	bash -c "which gifsicle || brew install gifsicle"
	asciicast2gif -S 2 -w 160 movie.cast movie.gif
