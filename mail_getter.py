from os.path import join, exists
from os import mkdir
import mailbox
import re
from email.header import decode_header
from email.utils import parseaddr
import quopri
from datetime import date


mbox_base_path = "/home/zsolt/Desktop/Dijnet/Takeout/Levelek"
# new_email_base = "/home/zsolt/Desktop/Dijnet/DijnetSzamlak_202305ig/billCommon/common"
# output_folder = "billCommon/common"
# output_folder_path = join(new_email_base, output_folder)
# todo: new_email_base-ben a dátumot cseréld ki .format(datetime.VALAMIRE), MERT, AKKOR NEM KELL CSERÉLGETNI A STRINGET
output_folder_path = "/home/zsolt/Desktop/Dijnet/DijnetSzamlak_{}ig/".format(date.today())
print("output_folder_path: ", output_folder_path)
if not exists(output_folder_path):
    mkdir(output_folder_path)


email_list = ['Befizetések-Díjnet számlák.mbox',
              'Befizetések.mbox',
              'Befizetések-Számla befizetések-Budapesti Távhőszol.mbox',
              'Befizetések-Számla befizetések-Díjbeszedő.mbox',
              'Befizetések-Számla befizetések.mbox']

def writer(payload, output_path):
    output_file_path = output_path + "all_letters_in_one_{}.txt".format(date.today())
    with open(output_file_path, "a+") as f:
        f.write(payload)



def decoder(mbox_path, output_path):
    # Open the mailbox file
    mbox = mailbox.mbox(mbox_path)
    # Loop through each email in the mailbox
    for message in mbox:
        # Decode the email sender
        decoded_sender = parseaddr(message['from'])[1]
        # Check if the email sender matches the search email address
        search_sender = "ugyfelszolgalat@dijnet.hu"
        if re.search(search_sender, decoded_sender, re.IGNORECASE) is not None:
            # Decode the subject of the email
            decoded_parts = decode_header(message['subject'])
            decoded_subject = ''
            for part, charset in decoded_parts:
                if charset:
                    decoded_subject += part.decode(charset)
                else:
                    decoded_subject += part
            # Check if the email subject matches the search subject
            if decoded_subject == 'Díjnet - Értesítés sikeres fizetésről':
                # Get the email payload
                payload = message.get_payload()
                # Decode the payload
                decoded_payload = ''
                if message.is_multipart():
                    for part in payload:
                        charset = part.get_content_charset()
                        if charset is None:
                            # We cannot know the character set so return decoded "something"
                            decoded_payload += part.get_payload(decode=True)
                        else:
                            decoded_payload += quopri.decodestring(part.get_payload()).decode(charset, errors="ignore")
                else:
                    charset = message.get_content_charset()
                    if charset is None:
                        # We cannot know the character set so return decoded "something"
                        decoded_payload = quopri.decodestring(payload.get_payload()).decode(errors="ignore")
                    else:
                        decoded_payload = quopri.decodestring(payload.encode()).decode(charset, errors="ignore")
                print("=================================================================================================")
                # Print the payload
                print(decoded_payload)
                writer(decoded_payload, output_path)

for mbox in email_list:
    mbox_path = join(mbox_base_path, mbox)
    print("##############################################################################xxxx")
    decoder(mbox_path, output_folder_path)

