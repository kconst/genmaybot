import time, sys

#test commit

def kill_bot(line, nick, self, c):
    print("got die command from " + nick)
    message = ""
    if line[4:]:
        message = line[4:]
    c.disconnect(message)
    self.t.cancel()
    sys.exit(0)
kill_bot.admincommand = "die"    

def nick(line, nick, self, c):
    print(line)
    print(line[5:])
    c.nick(line[5:])
nick.admincommand = "nick"

def clear_bans(line, nick, self, c):
    print(nick + " cleared bans")
    self.spam ={}
    return "All bans cleared"
clear_bans.admincommand = "clearbans"

def reload_modules(line, nick, self, c):
    return self.loadmodules()
    
reload_modules.admincommand = "reload"        

def enable_command(line, nick, self, c):
    if len(line.split(" ")) == 2:
        command = line.split(" ")[1]
        if command in self.commandaccesslist:
            del self.commandaccesslist[command]
            return command + " Enabled"
        else:
            return command + " not disabled"
enable_command.admincommand = "enable"

def disable_command(line, nick, self, c):
    if len(line.split(" ")) == 2:
        command = line.split(" ")[1]
        self.commandaccesslist[command] = "Disabled"
        return command + " Disabled"
disable_command.admincommand = "disable"

def cooldown_command(line, nick, self, c):
    if len(line.split(" ")) == 3:
        command = line.split(" ")[1]
        cooldown = line.split(" ")[2]
        if cooldown.isdigit():
            cooldown = int(cooldown)
            if cooldown == 0:
                if command in self.commandaccesslist:
                    del self.commandaccesslist[command]
                return command + " cooldown disabled"
            else:
                self.commandaccesslist[command] = cooldown
                self.commandcooldownlast[command] = time.time() - cooldown   
                return command + " cooldown set to " + str(cooldown) + " seconds (set to 0 to disable)"
        else:
            return "bad format: 'cooldown !wiki 30' (30 second cooldown on !wiki)"
    else:
        return "not enough perameters: cooldown !command ##"
cooldown_command.admincommand = "cooldown"

def command_status(line, nick, self, c):
    if len(line.split(" ")) == 2:
        command = line.split(" ")[1]
        if command in self.commandaccesslist:
            return command + " " + str(self.commandaccesslist[command]) + " (Seconds cooldown if it's a number)"
        else:
            return command + " Enabled"
    elif len(line.split(" ")) == 1:
        return str(list(self.commandaccesslist.items()))
    
command_status.admincommand = "status"

def join_chan(line, nick, self, c):
    if len(line.split(" ")) == 2:
        chan = line.split(" ")[1]
        if chan[0:1] != "#":
            return "not a valid channel name"
        if chan in self.channels:
            return "Already in " + chan
        else:
            c.join(chan)
            return "Joined " + chan
join_chan.admincommand = "join"

def part_chan(line, nick, self, c):
    if len(line.split(" ")) >= 2:
        chan = line.split(" ")[1]
        message = ""
        if len(line.split(" ")) > 2:
            message = " ".join(line.split(" ")[2:])
        if chan[0:1] != "#":
            return "not a valid channel name: Part #chan part message here"
        if chan in self.channels:
            c.part(chan, message)
            return "Left " + chan
        else:
            return "Not in " + chan
part_chan.admincommand = "part"

def say_cmd(line, nick, self, c):
	if len(line.split(" ")) > 2:
		chan = line.split(" ")[1]
		words = " ".join(line.split(" ")[2:])
		c.privmsg(chan, words)
		return "Said %s to %s" % (words, chan)
	else: 
		return "Correct syntax: say [#channel/nickname] I hate you!"
say_cmd.admincommand="say"

def show_channels(line, nck, self, c):
    return ", ".join(self.channels)
show_channels.admincommand = "channels"

