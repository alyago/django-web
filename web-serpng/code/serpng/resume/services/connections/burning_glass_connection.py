import os
import socket
import array
from struct import *		# for packing and unpacking functions
from django.conf import settings

"""
Connect to burning glass resume parsing service.

Provides a to_xml() method to turn a word, pdf or text file into the burning glass xml structure.
See burning glass documentation at .../platform-django/library/external/burning-glass

"""
class BurningGlassConnection(object):
  
    def __init__(self, host_address = settings.BURNING_GLASS_HOST, port = settings.BURNING_GLASS_PORT):      
        self.host_address = host_address
        self.port = port
           
           
    """
    Turn a word, pdf or text file as a string into the burning glass xml structure.

    Modified Sample function from burning glass
    This uses the Listener socket interface.
    
    Returns a tagged (parsed) resume as a utf8 xml structure.
    See the DTD at .../platform-django/library/external/burning-glass
    
    """
    def get_tagged_resume_string(self, resume_string):
          
        # Connect to the socket on the specified address/port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.connect((self.host_address, self.port))     

        # Build the command header.  This must be packed into network
        # byte order precisely as shown.
        # field     size    comment
        # length    4       12 + data size
        # flags     4       must be 0
        # version   2       must be 1
        # id        4       user value
        # type      2       8 -> tag-binary-doc
        h_length = 12 + len(resume_string) + 2
        h_flags = 0
        h_version = 1
        h_id = 0
        h_type = 8
        hdr = pack('>iihih', h_length, h_flags, h_version, h_id, h_type)

        # Create a binary array to hold the message.
        # We add the 'R' for resume and single null character for the hint.
        # We could extract the file extension and provide that as a hint,
        # but it is usually sufficient to let the system figure it out.
        msg = array.array('c',hdr)
        msg.append('R')
        msg.append('\0')
        msg.extend(array.array('c',resume_string))

        # Write tag command to Socket
        s.send(msg)

        # Read header (16 bytes) and unpack the information.
        # Use the adjusted length to read all the data.
        hdr = s.recv(16)
        (h_length, h_flags, h_version, h_id, h_type ) = unpack('>iihih', hdr)
        h_length = h_length - 12

        tagged = ""
        while h_length > 0:
            data = s.recv(h_length)
            if not data: break;
            h_length = h_length - len(data)
            tagged = tagged + data
            
        s.close()

        tagged_utf8 = tagged.decode('latin1').encode('utf-8')
          
        return tagged_utf8
            
