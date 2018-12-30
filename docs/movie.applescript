
tell application "Finder"
	set parentpath to POSIX path of (parent of (path to me) as string)
	set filename to name of (path to me)

	-- display dialog parentpath
	-- display dialog filename
end tell


tell application "iTerm"
	activate
	create window with default profile

	tell first session of current tab of current window
		set name to "rmux usage example"
		set columns to 80
		set rows to 40
		write text "cd ~ && rm -rf ~/os/foo && rm -f " & parentpath & "movie.cast && clear && asciinema rec " & parentpath & "movie.cast"
		my info_string("we are going to clone a git project")
		delay 2
		my write_string("git clone https://github.com/ssbarnea/foo.git ~/os/foo && cd ~/os/foo")
		delay 1
		my write_string("./foo.sh")
		delay 4
		my info_string("lets try to run the same remotely on two hosts")
		delay 3
		my write_string("HOSTS='n0 n2' rmux ./foo.sh")
		delay 8
		my info_string("so we are done, time to close our session by typing exit or pressing Ctrl-D")
		delay 4
	end tell

	tell application "System Events" to tell process "iTerm"
		keystroke "d" using control down -- close tmux
		delay 1
		keystroke "d" using control down -- close asciinema
		delay 1
		keystroke "d" using control down -- close terminal window
	end tell
end tell

on write_string(the_string)
	tell application "System Events" to tell process "iTerm"
		-- tell application "iTerm" to activate
		delay 1
		repeat with the_character in the_string
			keystroke the_character
			delay (random number from 0.03 to 0.1)
		end repeat
		delay 1
		key code 36
		key code 123 using command down
	end tell
end write_string


on info_string(the_string)
	tell application "System Events" to tell process "iTerm"
		-- tell application "iTerm" to activate
		delay 1
		repeat with the_character in the_string
			keystroke the_character
			delay (random number from 0.03 to 0.1)
		end repeat
		delay 1
		repeat with the_character in the_string
			key code 51
			delay (random number from 0.01 to 0.05)
		end repeat
	end tell
end info_string

on replace_chars(this_text, search_string, replacement_string)
	set AppleScript's text item delimiters to the search_string
	set the item_list to every text item of this_text
	set AppleScript's text item delimiters to the replacement_string
	set this_text to the item_list as string
	set AppleScript's text item delimiters to ""
	return this_text
end replace_chars
