import json
import boto3
import os
import urllib.parse

s3_client = boto3.client('s3')

def remove_metadata(text):
    """Tìm và cắt bỏ phần JSON Metadata ở đầu file, chỉ giữ lại từ Tiêu đề trở đi"""
    delimiter = "---METADATA_END---"
    if delimiter in text:
        return text.split(delimiter, 1)[1].lstrip()
    return text

def dynamic_split_blogs(original_text, translated_text, char_limit_en=1500): 
    """Tách Chunk theo Block Markdown trọn vẹn (Ngăn cách bởi \n\n)"""
    # Tách bài viết thành danh sách các đoạn (block)
    en_blocks = original_text.split('\n\n')
    vi_blocks = translated_text.split('\n\n')
    
    chunks = []
    en_len = len(original_text)
    vi_len = len(translated_text)
    
    if en_len == 0 or vi_len == 0: 
        return []
    
    en_idx = 0
    vi_idx = 0
    
    while en_idx < len(en_blocks) or vi_idx < len(vi_blocks):
        current_en_chunk = []
        current_vi_chunk = []
        current_en_size = 0
        
        # 1. Gom các block tiếng Anh cho đến khi chạm ngưỡng char_limit_en
        while en_idx < len(en_blocks):
            block = en_blocks[en_idx]
            current_en_chunk.append(block)
            current_en_size += len(block) + 2  # +2 bù cho ký tự \n\n đã bị split
            en_idx += 1
            if current_en_size >= char_limit_en:
                break
                
        # 2. Tính tỷ lệ để gom số block tiếng Việt tương ứng
        dynamic_ratio = vi_len / en_len if en_len > 0 else 1
        target_vi_size = current_en_size * dynamic_ratio
        current_vi_size = 0
        
        while vi_idx < len(vi_blocks):
            block = vi_blocks[vi_idx]
            current_vi_chunk.append(block)
            current_vi_size += len(block) + 2
            vi_idx += 1
            if current_vi_size >= target_vi_size:
                break
                
        # 3. Vét máng các block còn sót lại nếu 1 trong 2 bên đã cạn
        if en_idx >= len(en_blocks):
            while vi_idx < len(vi_blocks):
                current_vi_chunk.append(vi_blocks[vi_idx])
                vi_idx += 1
        if vi_idx >= len(vi_blocks):
            while en_idx < len(en_blocks):
                current_en_chunk.append(en_blocks[en_idx])
                en_idx += 1

        chunks.append({
            "original_text": '\n\n'.join(current_en_chunk).strip(),
            "translated_text": '\n\n'.join(current_vi_chunk).strip()
        })
        
    return chunks

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    try:
        detail = event.get('detail', {})
        bucket_name = detail.get('bucket', {}).get('name')
        translated_key = detail.get('object', {}).get('key')
        
        if not bucket_name or not translated_key:
            bucket_name = event.get('bucket')
            translated_key = event.get('key')
            
        translated_key = urllib.parse.unquote_plus(translated_key)
        file_name = os.path.basename(translated_key)
        original_key = f"original/{file_name}"
        article_id = file_name.replace('.md', '')

        # Tải nội dung
        trans_obj = s3_client.get_object(Bucket=bucket_name, Key=translated_key)
        orig_obj = s3_client.get_object(Bucket=bucket_name, Key=original_key)
        
        translated_text = trans_obj['Body'].read().decode('utf-8')
        original_text = orig_obj['Body'].read().decode('utf-8')

        # Gọt rác Metadata
        translated_text = remove_metadata(translated_text)
        original_text = remove_metadata(original_text)

        # Cắt nhỏ bài viết bằng logic Block mới
        chunks = dynamic_split_blogs(original_text, translated_text, char_limit_en=1500)
        print(f"Split into {len(chunks)} chunks.")
        
        output_payloads = []
        total_chunks = len(chunks)
        
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "chunk_index": i + 1,
                "total_chunks": total_chunks,
                "article_id": article_id,
                "original_text": chunk['original_text'],
                "translated_text": chunk['translated_text']
            }
            temp_key = f"processing/{article_id}/chunk_{i+1}.json"
            s3_client.put_object(
                Bucket=bucket_name, Key=temp_key,
                Body=json.dumps(chunk_data, ensure_ascii=False).encode('utf-8'),
                ContentType='application/json'
            )
            output_payloads.append({
                "s3_bucket": bucket_name, "s3_key": temp_key,
                "chunk_index": i + 1, "article_id": article_id
            })

        return output_payloads

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e