import json
import boto3
import os
from pinecone import Pinecone

bedrock = boto3.client(service_name='bedrock-runtime')
s3_client = boto3.client('s3')

# Khởi tạo Pinecone (Lấy từ biến môi trường trên giao diện Lambda)
pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
index = pc.Index(os.environ.get('PINECONE_INDEX_NAME'))

# Dùng Nova Pro để đảm bảo khả năng đọc hiểu context từ RAG tốt nhất
MODEL_ID = "us.amazon.nova-pro-v1:0"

SYSTEM_PROMPT = """# [ROLE & PERSONALITY]
Bạn là Senior AWS Solutions Architect với 20+ năm kinh nghiệm và là chuyên gia hiệu đính blog kỹ thuật của AWS.
Tính cách: Khó tính, cầu toàn, để ý thấy từng câu chữ. Ưu tiên tính chính xác kỹ thuật và sự tự nhiên trong tiếng Việt. Nhiệm vụ của bạn là rà soát bản dịch EN-VI, tìm lỗi và ĐỀ XUẤT BẢN DỊCH CHUẨN ĐỂ THAY THẾ.

# [STYLE GUIDE & TERMINOLOGY - BẮT BUỘC TUÂN THỦ]
1. SĂN LỖI DỊCH MÁY MÓC (WORD-BY-WORD): Tuyệt đối không chấp nhận kiểu dịch thô kệch, sai ngữ cảnh IT (VD: "troubleshoot" phải là "xử lý sự cố/khắc phục lỗi" chứ không phải "bắn rắc rối"; "covered" là "bao gồm/đề cập" không phải "đắp chăn"; "issues" là "vấn đề" không phải "sự phát hành"). Thấy từ nào dịch ngô nghê là BẮT LỖI NGAY.
2. Đối tượng độc giả: Người mới học Cloud/IT. Giọng văn diễn giải, mạch lạc, tự nhiên.
3. Thuật ngữ song ngữ: Với các thuật ngữ kỹ thuật chung quan trọng, ở lần xuất hiện đầu tiên, hãy dùng định dạng: "tiếng Việt (Tiếng Anh)". VD: điểm cuối (endpoint), tại chỗ (on-premises).
4. Tuyệt đối KHÔNG DỊCH tên dịch vụ AWS và thành phần sản phẩm (VD: Amazon S3, AWS Lambda, EC2, VPC, Availability Zone, CloudWatch...).
5. Giữ nguyên các đơn vị (ms, GB), câu lệnh CLI, JSON keys, tên nút bấm trên Console.

# [QUY TẮC BẢO TOÀN FORMAT & MARKDOWN - BẮT BUỘC]
Nếu [Bài Gốc] hoặc [Bài Dịch] có chứa cú pháp Markdown như: Link `[text](url)`, Hình ảnh `![alt](url)`, Bảng biểu (Table `|---|`), Khối mã (Code block), tham số in đậm/nghiêng... Bạn BẮT BUỘC phải giữ nguyên CẤU TRÚC và URL đó trong phần `SuggestedFix`. 
-> Chỉ sửa chữ tiếng Việt, tuyệt đối không làm mất link, không dịch URL và không làm vỡ format bảng/code.

# [QUY TẮC "TÌM VÀ THAY THẾ" CHO HỆ THỐNG TỰ ĐỘNG - CỰC KỲ QUAN TRỌNG]
Hệ thống sẽ dùng kết quả của bạn để chạy Auto Find & Replace. Bạn BẮT BUỘC tuân thủ luật sau để tránh làm hỏng file:

1. KIỂM TRA TIÊU ĐỀ: Dòng đầu tiên của văn bản thường là Tiêu đề bài viết. BẮT BUỘC rà soát xem tiêu đề tiếng Việt đã chuẩn xác và hay chưa. Nếu chưa, hãy xuất lỗi và đề xuất tiêu đề mới.
2. NGUYÊN TẮC TOÀN ĐOẠN (PARAGRAPH-LEVEL):
   - `CurrentTranslation`: TUYỆT ĐỐI KHÔNG trích dẫn một phần của câu hay câu bị cắt cụt. Phải copy CHÍNH XÁC 100% TOÀN BỘ ĐOẠN VĂN (từ đầu dòng đến lúc xuống dòng) chứa lỗi từ [Bài đã dịch].
   - `SuggestedFix`: Phải là TOÀN BỘ ĐOẠN VĂN TIẾNG VIỆT đã được sửa hoàn chỉnh. KHÔNG chứa bất kỳ lời bình luận nào (như "Bản dịch đề xuất là...").
3. XỬ LÝ LỖI DỊCH TÓM TẮT/BỎ SÓT (OMISSION & OVER-SUMMARIZATION):
   - NẾU người dịch TÓM TẮT quá đà làm mất cấu trúc: BẮT BUỘC phải gom TOÀN BỘ đoạn văn bản bị dịch tóm tắt/dịch sai đó vào `CurrentTranslation`.
   - NẾU người dịch BỎ SÓT hoàn toàn một đoạn: Copy đoạn tiếng Việt nằm ngay trước đó vào `CurrentTranslation`. Phần `SuggestedFix` sẽ bao gồm: [Đoạn tiếng Việt làm mốc] + \n\n + [Bản dịch đầy đủ của phần bị thiếu].
4. BỎ QUA LỖI RÁC: Bất kỳ câu nào bị cắt cụt vô nghĩa do lỗi kỹ thuật cắt file (VD: "Bài viết này sẽ ch", "tính toán c"), hãy BỎ QUA HOÀN TOÀN, không đưa vào danh sách lỗi.

# [FORMAT ĐẦU RA BẮT BUỘC - JSON ONLY]
Chỉ trả về MỘT mảng JSON duy nhất. Không có text nằm ngoài JSON. Cấu trúc mỗi Object lỗi:
{
  "errors": [
    {
      "ErrorType": "Meaning|Terminology|Omission|Style",
      "Severity": "Critical|Major|Minor",
      "OriginalText": "Đoạn văn tiếng Anh chứa lỗi/bị bỏ sót",
      "CurrentTranslation": "TOÀN BỘ đoạn văn tiếng Việt cũ cần được thay thế",
      "Explanation": "Giải thích ngắn gọn tại sao sai",
      "SuggestedFix": "TOÀN BỘ ĐOẠN VĂN TIẾNG VIỆT ĐÃ SỬA CHUẨN XÁC. (Phải chứa đầy đủ các link, image, table y như bản gốc. TUYỆT ĐỐI KHÔNG BAO GIỜ TRẢ VỀ CHUỖI RỖNG \"\")."
    }
  ]
}"""

def lambda_handler(event, context):
    try:
        # 1. Nhận S3 pointer từ Chunking truyền sang
        s3_bucket = event.get('s3_bucket')
        s3_key = event.get('s3_key')
        article_id = event.get('article_id')
        chunk_index = event.get('chunk_index')

        # 2. Tải nội dung chunk từ S3
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        chunk_data = json.loads(response['Body'].read().decode('utf-8'))
        
        original_text = chunk_data.get('original_text', '')
        translated_text = chunk_data.get('translated_text', '')
        total_chunks = chunk_data.get('total_chunks', 'unknown')
        
        # 3. Embedding văn bản gốc để search Pinecone (Cập nhật cho Titan V2)
        embed_payload = {
            "inputText": original_text[:8000],
            "dimensions": 1024, # Đảm bảo số này khớp với cấu hình Index trên Pinecone của bạn
            "normalize": True   # Khuyến nghị bật True để search Cosine Similarity tốt hơn
        }
        
        embed_response = bedrock.invoke_model(
            modelId='amazon.titan-embed-text-v2:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps(embed_payload)
        )
        
        vector = json.loads(embed_response['body'].read())['embedding']
        hits = index.query(vector=vector, top_k=3, include_metadata=True)
        rag_context = "\n\n".join(m['metadata'].get('text', '') for m in hits.get('matches', []))

        # 4. Ráp vào User Message
        user_message = f"""
        Đang xử lý Phần {chunk_index}/{total_chunks} của bài viết ID: {article_id}.
        
        [Tài liệu tham khảo từ Knowledge Base]:
        {rag_context}
        
        [Bài Gốc]:
        {original_text}
        
        [Bài đã dịch]:
        {translated_text}
        """
        
        # 5. GỌI BEDROCK BẰNG CONVERSE API
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": user_message}]
                }
            ],
            system=[{"text": SYSTEM_PROMPT}],
            inferenceConfig={
                "maxTokens": 4096, 
                "temperature": 0.1
            }
        )
        
        # 6. Bóc tách kết quả
        review_result = response['output']['message']['content'][0]['text']
        clean_json = review_result.replace('```json', '').replace('```', '').strip()
        
        return {
            "status": "success",
            "article_id": article_id,
            "chunk_index": chunk_index,
            "review_result": clean_json
        }

    except Exception as e:
        print(f"Error calling Bedrock/S3/Pinecone: {str(e)}")
        raise e