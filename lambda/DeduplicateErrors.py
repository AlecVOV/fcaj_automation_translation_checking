import json
import difflib
import re # Thêm thư viện Regex để tìm JSON

def is_similar(str1, str2, threshold=0.9):
    if not str1 or not str2: return False
    return difflib.SequenceMatcher(None, str1, str2).ratio() > threshold

def extract_json_array(text):
    """Tìm và trích xuất mảng JSON từ chuỗi văn bản bất kỳ"""
    try:
        # Tìm đoạn bắt đầu bằng [ và kết thúc bằng ]
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []
    except Exception as e:
        print(f"Không thể trích xuất JSON: {e}")
        return []

def lambda_handler(event, context):
    all_chunks_results = event 
    all_errors = []
    
    # In ra để ông check trong log xem AI thực sự trả về cái gì
    print("DEBUG - FULL INPUT FROM MAP:", json.dumps(all_chunks_results))
    
    for result in all_chunks_results:
        raw_result = result.get('review_result', '')
        # Dùng hàm extract_json_array mới để an toàn hơn
        errors_in_chunk = extract_json_array(raw_result)
        
        for e in errors_in_chunk:
            e['article_id'] = result.get('article_id')
            all_errors.append(e)

    if not all_errors:
        print("CẢNH BÁO: Không tìm thấy lỗi nào trong toàn bộ các chunk!")
        return {"article_id": all_chunks_results[0].get('article_id'), "clean_errors": []}

    # Logic lọc trùng giữ nguyên
    unique_errors = []
    for current_error in all_errors:
        is_duplicate = False
        for saved_error in unique_errors:
            if (current_error.get('ErrorType') == saved_error.get('ErrorType') and 
                is_similar(current_error.get('OriginalText'), saved_error.get('OriginalText'))):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_errors.append(current_error)

    print(f"KẾT QUẢ: Tổng {len(all_errors)} lỗi -> Sạch {len(unique_errors)} lỗi.")
    return {
        "article_id": all_chunks_results[0].get('article_id'),
        "clean_errors": unique_errors
    }