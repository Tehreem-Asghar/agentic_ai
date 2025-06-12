# 📦 Structured Outputs with Pydantic - OpenAI Agents SDK

Structured output ka matlab hai ke tumhara agent sirf normal text nahi balkay ek proper format mein data return kare — jaise ke JSON ke andar specific fields. Ye cheez bohat zaroori hoti hai jab tum kisi system ya automation flow ke saath kaam kar rahi ho.

---

## ✅ Structured Output kyu use karein?

1. **Data Parsing Asaan Ho Jata Hai**  
   - Tumhe complicated text extract karne ki zarurat nahi padti.  
   - Direct fields mil jati hain jaise: `order_id`, `reason`, etc.

2. **Easy Integration**  
   - Tum structured data ko APIs ya databases ke saath direct connect kar sakti ho.

3. **Reliable Aur Consistent Format**  
   - Har baar same structure mein response milta hai.  
   - Koi ghalat ya missing field nahi hoti.

4. **Automation Friendly**  
   - Tum apne workflows automate kar sakti ho, jaise refund request ya form submission, jo data points pe depend karte hain.

---

## 🔄 Structured Output vs. JSON Mode

| Feature               | JSON Mode (Simple)            | Structured Output (Pydantic)       |
|-----------------------|-------------------------------|------------------------------------|
| JSON Validity         | ✅ Sirf valid JSON deta hai   | ✅ Valid JSON + schema follow karta hai |
| Schema Follow?        | ❌ Nahi karta                  | ✅ Hamesha karta hai               |
| Reliable Data Access  | ❌ Kabhi fields missing hoti  | ✅ Hamesha complete data deta hai |
| Best For              | Sirf testing ya debugging     | Real system ya automation flows   |

---

## 🛠️ Example: Pydantic ke saath use

```python
from pydantic import BaseModel

class RefundInfo(BaseModel):
    order_id: str
    reason: str
