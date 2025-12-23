"""
mock_llm.py
Simulates OpenAI API behavior for testing/demo purposes.
"""
import random

class MockOpenAI:
    def __init__(self, api_key=None):
        self.api_key = "mock-key"

    class chat:
        class completions:
            @staticmethod
            def create(model, messages, temperature=0.7):
                # Extract last message to determine context
                last_msg = messages[-1]['content']
                system_msg = messages[0]['content'] if messages else ""
                
                response_text = ""
                
                # Simple heuristic to determine type of request based on prompt content
                if "구체적인 행동이나 발화 의도" in last_msg: # Planner Prompt
                    plans = [
                        "상대방의 말에 맞장구친다.",
                        "주제를 날씨로 돌린다.",
                        "자신의 고민을 털어놓는다.",
                        "커피를 마시자고 제안한다.",
                        "농담을 던져 분위기를 띄운다."
                    ]
                    response_text = random.choice(plans)
                    
                elif "새롭게 알게 된 사실" in last_msg: # Reflection Prompt
                    response_text = "특별한 변화는 감지되지 않음. 평온한 상태 유지."
                    
                elif "발화:" in last_msg: # Utterance Prompt
                    # Min-jun specific
                    if "Min-jun" in system_msg:
                        responses = [
                            "아아! 삶은 고통과 환희의 연속이군요!",
                            "당신의 그 말, 제 영혼을 울리는군요.",
                            "커피, 그것은 검은 눈물과도 같죠...",
                            "(비장하게) 오늘 날씨가 마치 제 마음 같네요."
                        ]
                        response_text = random.choice(responses)
                    # Seo-yeon specific
                    elif "Seo-yeon" in system_msg:
                        responses = [
                            "커피 없인 대화도 없습니다.",
                            "마감이 급해서 짧게 말할게요.",
                            "그 드라마틱한 톤 좀 자제해 줄래요?",
                            "네네, 아주 감동적이네요. (영혼 없음)"
                        ]
                        response_text = random.choice(responses)
                    else:
                        response_text = "음, 그렇군요. 흥미로워요."
                        
                else:
                    response_text = "Mock LLM Response: 상황을 이해했습니다."
                
                # Mock response object structure mimicking OpenAI
                return MockResponse(response_text)

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content
