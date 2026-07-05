"""Extract text from .doc (OLE Compound Document) - fixed version."""
import olefile
import struct
import sys
import re

def extract_text(doc_path):
    ole = olefile.OleFileIO(doc_path)
    word_stream = bytearray(ole.openstream('WordDocument').read())
    
    # Read table stream
    table_name = '1Table' if ole.exists('1Table') else '0Table'
    table_data = bytearray(ole.openstream(table_name).read())
    
    # FIB info
    ccpText = struct.unpack_from('<I', word_stream, 0x004C)[0]
    
    # fcClx is at offset 0x01A2 in WordDocument (FIB)
    fcClx = struct.unpack_from('<I', word_stream, 0x01A2)[0]
    lcbClx = struct.unpack_from('<I', word_stream, 0x01A2 + 4)[0]
    
    # Read CLX from table stream
    clx = table_data[fcClx:fcClx + lcbClx]
    
    # Parse CLX to find Pcdt (type 0x02)
    pos = 0
    while pos < len(clx):
        clxt = clx[pos]
        if clxt == 0x01:  # Prc
            cb = struct.unpack_from('<H', clx, pos + 1)[0]
            pos += 3 + cb
        elif clxt == 0x02:  # Pcdt
            lcb = struct.unpack_from('<I', clx, pos + 1)[0]
            pcdt = clx[pos + 5:pos + 5 + lcb]
            break
        else:
            pos += 1
    else:
        raise ValueError("Pcdt not found")
    
    # PlcPcd: array of CPs (n+1) * 4 bytes, then PCDs n * 8 bytes
    # Last 4 bytes of PlcPcd is reserved
    n = (len(pcdt) - 4) // (4 + 8)  # subtract the 4 reserved bytes
    # Actually, PlcPcd = (n+1) CPs + n PCDs, total = (n+1)*4 + n*8
    # Rearranged: total = 4n + 4 + 8n = 12n + 4
    # n = (total - 4) // 12
    n = (len(pcdt) - 4) // 12
    
    result = []
    for i in range(n):
        cp_start = struct.unpack_from('<I', pcdt, i * 4)[0]
        cp_end = struct.unpack_from('<I', pcdt, (i + 1) * 4)[0]
        
        pcd_offset = (n + 1) * 4 + i * 8
        
        # PCD structure:
        # offset 0: short (2 bytes) - reserved
        # offset 2: FC (4 bytes) - fcCompressed
        fc_compressed = struct.unpack_from('<I', pcdt, pcd_offset + 2)[0]
        
        is_unicode = not bool(fc_compressed & 0x40000000)
        fc = fc_compressed & 0x3FFFFFFF
        
        char_count = cp_end - cp_start
        
        if is_unicode:
            # fc is character offset, convert to byte offset
            byte_fc = fc * 2
            byte_count = char_count * 2
            raw = bytes(word_stream[byte_fc:byte_fc + byte_count])
            text = raw.decode('utf-16-le', errors='replace')
        else:
            byte_fc = fc
            raw = bytes(word_stream[byte_fc:byte_fc + char_count])
            # Try cp1252 first (Windows ANSI), then latin-1
            try:
                text = raw.decode('cp1252')
            except:
                text = raw.decode('latin-1', errors='replace')
        
        result.append(text)
    
    ole.close()
    return ''.join(result)


if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\数据要素X\青气测函〔2026〕55号\_notice.doc'
    text = extract_text(path)
    out = r'D:\workbuddy\project_数据要素X\code\_notice_v2.txt'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Extracted {len(text)} chars. First 200:")
    print(repr(text[:200]))
