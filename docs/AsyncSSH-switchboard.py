#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import asyncio, asyncssh, sys, os, time, copy, psutil, subprocess
from datetime import datetime, timezone, tzinfo
import pytz
from typing import List, cast, Optional

# import logging
# logging.basicConfig(level='DEBUG')
# asyncssh.set_debug_level(2)
# asyncssh.set_log_level(5)

#print(f'Python Version={sys.version_info}')

passwords = {'device': '#!&+cs',
             '$admin': 'as'
            }
maxHist = 10        # keep this number of received lines for each device
admins = set([])    # list of all online admins
online = {}         # keep track of station=>process map
shuttingDown = False
led_state = 'none'

class TooSoon(Exception):
    "Raised when we can't start SSH on existing ports"
    pass

class ExitNow(Exception):
    "#EXIT command encountered"
    pass

def timeStamp():
    return "[" + datetime.now().strftime("%m-%d %H:%M:%S") + "] "

def get_free_memory():
    return psutil.virtual_memory().available

def uppercase_outside_quotes(text):
    result = []
    inside_quotes = False
    for char in text:
        if char == '"':
            inside_quotes = not inside_quotes
        if not inside_quotes:
            char = char.upper()
        result.append(char)
    return ''.join(result)
  
def is_ip_reachable(ip):
    if os.system(f'ping {ip} -w 5 > clear') == 0:
        return True  # IP is reachable
    else:
        return False  # IP is not reachable
    
def green_flasher():
    global led_state          # flip it each time we are called
    
    if led_state == 'none':
        led_state = 'default-on'
    else:
        led_state = 'none'
        
    result = subprocess.run("echo " + led_state + " > /sys/class/leds/green_led/trigger", 
                            capture_output=False, shell=True, text=True)

def getZone(timezone_name):
    timezone = pytz.timezone(timezone_name)
    naive_now = datetime.now()  # Create a naive datetime without timezone info
    localized_now = timezone.localize(naive_now)  # Localize the naive datetime
    offset = localized_now.utcoffset()
    # Convert the offset into hours
    offset_hours = int(round(offset.total_seconds() / 3600))
    if offset_hours == -8:
        return ("PST+8")
    else:
        return("PDT+7")
    
if sys.platform == 'win32':
    port = 8022; key_path = 'C:/Users/'+os.getlogin()
else:      # suppose we are linux
    ports = [22, 8022]; key_path = '/home/' + 'harry'   #  os.getlogin()
    
os.chdir(key_path)
if not os.path.exists(key_path + '/OTA'):
    os.mkdir(key_path + '/OTA')
for dir in ['console', 'repeater', 'tbeam', 'raw', 'tbeam1262', 'tdeck', 'twatch']:
    dirX = key_path + '/OTA/' + dir   
    if not os.path.exists(dirX):
        os.mkdir(dirX)
# print('Default dir = '+os.getcwd())

is_online = is_ip_reachable('8.8.8.8')   # google DNS

class MySFTPServer(asyncssh.SFTPServer):
    
    def __init__(self, chan: asyncssh.SSHServerChannel):
        self._chroot = None
        self._ip = chan.get_extra_info('peername')[0]
        self._username = chan.get_extra_info('username')
        print(timeStamp() + f'IP {self._ip} SCPing as user {self._username}' )
        
    async def open(self, path, pflags, attrs):
        # Open the file and return an SFTPFile object
        file_obj = super().open(path, pflags, attrs)
        self.file_obj = file_obj
        self.path = path.decode()
        self.milestone = 10   # message at 10% etc.
        #print("Opened....",self.path)
        return file_obj

    async def read(self, handle, offset, length):
        # Perform the read operation
        data = super().read(handle, offset, length)
        #print("Reading @", offset)
        
        if offset == 0:
            # Get the file object from the handle
            file_obj = self.file_obj

            file_stats = self.stat(self.path)

            # Access the file size from the file stats
            self.file_size = file_stats.st_size
            if not is_online: print(f'Reading from file: {self.path}, Size: {self.file_size} bytes')
        progress = int(100*(offset+length)/self.file_size)
        if progress >= self.milestone:
            if not is_online: print(f'...{progress}%', end=" ")
            self.milestone = min(progress + 10, 100)
        if self.file_size == offset + length:
            if not is_online: print()
            print(timeStamp() + f'IP {self._ip} Download complete.')
        return data

class MySSHServer(asyncssh.SSHServer):
    
    def undo_connection(self):
        global online
        # print(timeStamp() + f'{self._username} has disconnected.')
        if self._username == None:            # it was never authenticated
            return
        if self._username == '$admin':
            # somehow we need to remove any links going to this specific admin but not others
            return
        if self._username != None and self._username in online:
            online[self._username]._process.close()       # stops sending keepalives?
            online.pop(self._username)              # no longer online
            for adm in admins:
                if adm._default == self._username:    # am I the default for any admin?
                    adm.write(timeStamp() + 'Default %s disconnected.' % self._username)
                    # print('removing default...')
                    adm._default = None               # if so, get rid of it
                if adm._answerback == self._username:
                    # print('removing answerback...')
                    adm._answerback = None
        
    def connection_made(self, conn: asyncssh.SSHServerConnection) -> None:
        self._conn = conn
        self._username = None
        self._ip = conn.get_extra_info('peername')[0]
        conn.set_keepalive(10,3)          # set keepalive parameters for this specific connection (30 seconds)
        print(timeStamp() + 'SSH connection received from %s.' % self._ip + 
            f" Free memory: {get_free_memory() / (1024 ** 3):.3f} GB")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(timeStamp() + 'SSH connection lost.' + f' [stationID={self._username} IP={self._ip}] exc={str(exc)}')
        if exc:
            if "Client not responding to keepalive" in str(exc):
                if self._username != None:
                    for adm in admins:
                        adm.write(timeStamp() + '%s not responding to keepalive.' % self._username)
                self.undo_connection()
                self._conn.close()
                return 
            if "[Errno 104]" in str(exc):
                self.undo_connection()
                self._conn.close()
                return                    # need to close this connection
            if 'Connection went down.' in str(exc):
                print('*******')     # catch why we crash
        self.undo_connection()
        self._conn.close()
            
    def begin_auth(self, username: str) -> bool:
        #global shuttingDown
        if shuttingDown:
            raise asyncssh.DisconnectError(asyncssh.DISC_CONNECT_BY_APPLICATION, "SwitchBoard is shutting down")
            return False
        self._username = username
        print(timeStamp() + f'IP {self._ip} connecting as user {self._username}' )
        # Password auth is required
        return True

    def password_auth_supported(self) -> bool:
        return True

    def validate_password(self, username: str, password: str) -> bool:
        if not is_online: print('Validating PWD',username, password)
        if username.isnumeric():
            if int(username) > 0 & int(username) <256:
                pw = passwords.get('device')
                # print(f'password={password}')
                return password == pw
        elif (username == '$admin'):
            pw = passwords.get('$admin')
            return password == pw
        else:
            self._conn.close()
            return False
            
    def auth_completed(self) -> None:
        global online
        # print(f'Authorized....{self._username}')
        if self._username in online:
                # print(f'Connection already exists for {self._username}')
                for admin in admins:
                    admin.write(timeStamp() + f'Closing previous connection for {self._username}.')
                    # print(f'username = {self._username} default = {admin._default}')
                    if admin._default == self._username:
                        online[self._username]._toAdmin = admin    # save this for next connection
                online[self._username]._process.close()
                online.pop(self._username, None)
        return

class SSHClient:

    def __init__(self, process: asyncssh.SSHServerProcess):
        self._process = process
        self._username = process.get_extra_info('username')     # get the user name
        self._ip = process.get_extra_info('peername')[0]   # ip address
        self._history = []
        self._default = None      # Admin: station # of any default I have set
        self._answerback = None   # Admin: station # for temporary command
        self._toAdmin = None      # Device: process id of any admin
                
    async def readline(self) -> str:
        return await cast(str, self._process.stdin.readline())

    def write(self, msg: str) -> None:
        # print(f'to device {self._username} [{msg.strip()}]')
        if not is_online: print(f'to device {self._username} [{msg.strip()}]')
        try:
            ret = self._process.stdout.write(msg.strip()+'\n') # need to get rid of return value
        except:    # seems like a connection went down
            pass   # unclear what to do here....
            #raise AssertionError("Connection went down.")
        
    def adminsWrite(self, msg: str) -> None:
        #print(f'Writing to admins: [{msg.strip()}]')
        for admin in admins:
            admin.write(msg)
            
    def forward(self, target: str, msg: str) -> None:
        global online
        # print(f'forwarding to {target} [{msg.strip()}]')
        if target == None:
            self.write(f'Default target not set.')
        elif online.get(target,None) != None:
            online[target].write(msg)
        else: self.write(f'{target} not online.') 
            
    def getHistory(self) -> list:
        return self._history
    
#     def mapOutput(self, source: str) -> None:
# #         for src, adm in self._toAdmin.items():
# #             if src == source and adm != self:
# #                 self._toAdmin.pop(src)
# #                 adm._default = None
#         self._toAdmin[source] = self
#         print(f'toAdmin={self._toAdmin}')
                
    @classmethod
    async def handle_client(cls, process: asyncssh.SSHServerProcess):
        # print('handle_client called')  # debug
        await cls(process).run()
        
    async def run(self) -> None:
        global online, admins
        #global shuttingDown

        if self._username == '$admin':               # admin I/O
            #self._process.channel.set_line_mode(True)
            #self._process.channel.set_echo(True)
            
            self.write(f'{len(online.keys())} devices are connected.')
            admins.add(self)
            self._default = None
            self._answerback = None
            while not self._process.stdin.at_eof():
                try:            # reading from admin station
                    async for line_in in self._process.stdin:
                        
                        # a new input line cancels an answerback
                        if self._answerback != None:
                            online[self._answerback]._toAdmin = None
                        if self._default != None:
                            online[self._default]._toAdmin = self
                        line = uppercase_outside_quotes(line_in.strip())
                        # print(f'line from {self._username} ['+line+']')
                        if len(line) == 0: continue
                        if not is_online: print('admin command ['+line+']')
                        if line.startswith('#'):
                            line = line[1:]
                            if line == "LIST":
                                online_list = sorted([int(x) for x in list(online.keys())])
                                self.write(' '.join([str(x) for x in online_list]))
                            elif line == "END":
                                self._default = None
                            elif line == "EXIT":    # shutdown all connections and the server itself
                                shuttingDown = True
                                raise ExitNow
                                return
                            elif line == "LAST":
                                if self._default == None:
                                    self.write('Default target not set.')
                                else:
                                    if online.get(self._default) != None:
                                        for hist in online.get(self._default).getHistory():
                                            self.write('%s: %s' % (self._default, hist))
                            elif line.isnumeric():    # log the admin to this station
                                if line in online:    # line is the station
                                    for a in admins:     # make sure no other admin has this default
                                        if a._default == line:
                                            a._default = None
                                        if a._answerback == line:
                                            a._answerback = None
                                    for d in online:
                                        if online[d]._toAdmin == self:
                                            online[d]._toAdmin = None
                                    self._default = line
                                    self._answerback = line
                                    online.get(line)._toAdmin = self
                                    # print(f'default={self._default}')
                                else: self.write(f'{line} not online.')  
                            else:
                                onetime = line_in[1:].strip().split(' ',1)
                                if onetime != None:
                                    # print(onetime)
                                    if onetime[0].isnumeric():
                                        if onetime[0] in online:
                                            self._answerback = onetime[0]  # will undo this on next input command
                                            online[onetime[0]]._toAdmin = self
                                            ##if self._default != None:
                                                ##online[self._default]._toAdmin = None  # don't monitor default until next input line
                                            # print(f'onetime answerback={onetime[0]}')
                                            self.forward(onetime[0], onetime[1])   # send the command and get replies
                                        else: self.write(f'{onetime[0]} not online.')
                                    else: self.write('not a command.')

                        else:  # doesn't start with #......
                            self.forward(self._default, line_in)    # send the command to a connected device
                except asyncssh.BreakReceived:
                    sys.exit(100)
                except asyncssh.TerminalSizeChanged as exc:
                    print(timeStamp() + f'Terminal size changed [stationID={self._username} IP={self._ip}]')
                    continue
                except ExitNow:
                    # print("ExitNow caught")
                    for device in online:
                        # print("Closing",device)
                        online[device]._process._conn.close()
                    for admin in admins:
                        # print("Closing","admin")
                        admin._process._conn.close()
                    exit(0)

    ############# device I/O  ####################
        else:
            if self._username in online:
                # print(f'Connection already exists for {self._username}')
                self.adminsWrite(timeStamp() + f'Closing previous connection for {self._username}.')
                online[self._username]._process.close()
            try:
                self._toAdmin = online[self._username]._toadmin  # use former connection, if any
            except:
                pass
            online[self._username] = self
            self.adminsWrite(timeStamp() + 'Device %s now connected.' % self._username)
            self._process.channel.set_line_mode(True)
            self._process.channel.set_echo(False)

            # if we are getting NTP time, then send it out
            if is_online:
                myZone = "US/Pacific"
                now = datetime.now(pytz.timezone(myZone))
                epoch = int(now.timestamp())   # send UTC time to devices
                #print(f'epoch {epoch} now is {datetime.now().strftime("%m-%d %H:%M:%S")} {now.tzname()}')
                self.write('set epoch ' + str(epoch))
                await asyncio.sleep(1)   # make sure it is processed
                self.write(f'send tz "{getZone(myZone)}" to {self._username}')  # this might set a new timezone
                await asyncio.sleep(1)   # make sure it is processed
            try:
                async for line in self._process.stdin: # reading from remote output
                        line = line.strip()
                        if len(line) == 0: 
                            continue    # lines which are blanks\n are ignored
                        if not is_online: print(f'line from {self._username} [{line}]')
                        self._history.append(line)
                        if (len(self._history) > maxHist):
                            del self._history[0] 
                        if len(line) != 0 and self._toAdmin != None:    # is an admin listening to me?
                            try:
                                # print(f'Sending line to {self._toAdmin._username}')  # debug
                                self._toAdmin.write('%s: %s' % (self._username, line))  # copy response to admin screen
                            except AssertionError:
                                print(f'Output to {self._username} failed.')
                                admins.discard(self._toAdmin)  # this admin went bye bye
                                self._default = None
                                self._answerback = None
                                self._toAdmin = None
                        if not line.startswith('#update_if_newer '): continue
                        currently = line.split(' ');
                        try:
                            if len(currently) != 5: raise TypeError("Can't update. Bad update_if_newer formet.")
                            if currently[1] != 'model': raise TypeError("Can't update. Missing model.")
                            if currently[3] != 'build': raise TypeError("Can't update. Missing build.")
                            current_build = float(currently[4])
                            # print('model=%s build=%s' % (currently[2], currently[4]))
                            OTA_path = 'OTA/%s/' % currently[2]
                            latest_file = OTA_path + 'latest.txt'
                            if not os.path.isfile(latest_file): raise TypeError("Can't update. Missing latest.txt")
                            with open(latest_file, "r") as f:
                                latest = f.readline().strip().split('=')
                            if len(latest) != 2: raise TypeError("Can't update. Bad latest.txt format.")
                            if latest[0] != 'build': raise Exception("Can't update. Bad latest.txt format.")
                            latest_build = float(latest[1])
                            if not is_online:
                                print('for model %s latest build is %.2f current build is %.2f' % (currently[2],latest_build,current_build))
                            if latest_build > current_build: # send the command to a connected device
                                # print('need to issue [update %s] command' % latest[1])  # debug
                                self.write('update %s' % latest[1])
                        except TypeError as exc:
                            self.write('echo "%s"' % exc)   # send error text back to user device
                            continue
            except asyncssh.BreakReceived:
                online.pop(self._username, None)
                self.adminsWrite(timeStamp() + 'Device %s has disconnected.' % self._username)

async def start_server(port) -> None:
    print('starting %s server on port %d' % (sys.platform, port))
    try:
        await asyncssh.create_server(MySSHServer,'', port,
            server_host_keys=[key_path+'/.ssh/ssh_host_rsa_key'],
            process_factory=SSHClient.handle_client,
            sftp_factory=MySFTPServer,
            keepalive_interval=10, keepalive_count_max=6, allow_scp=True)   # allow 60 seconds max                                   
    except OSError:
        # Too soon to restart
        raise TooSoon

async def flash_forever():
# Keep the main coroutine running indefinitely
    while True:
        if not is_online: green_flasher()          # change the state of the green LED
        await asyncio.sleep(5)   # every 5 seconds       

async def linux_main():
    await asyncio.gather(
        start_server(ports[0]),
        start_server(ports[1]))
    await asyncio.create_task(flash_forever())

if __name__ == '__main__':
    while True:
        try:
            if sys.platform == 'win32':
                loop = asyncio.get_event_loop()
                loop.create_task(start_server(port))
                break      # it started
            else:
                asyncio.run(linux_main())
                break
        except TooSoon:
            print("Can't start server yet...")
            time.sleep(15)


# In[ ]:




