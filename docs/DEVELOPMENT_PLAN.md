# 🛠️ CoinFlow Bot - Development Plan for v2.2-v2.5

**Document Version:** 1.0  
**Last Updated:** October 19, 2025  
**Status:** Planning Phase

---

## 📋 Executive Summary

This document outlines the technical implementation plan for CoinFlow Bot versions 2.2 through 2.5, based on the comprehensive technical specification received. The plan spans 6 major features across 4 versions over 12 months (November 2025 - October 2026).

### Current Status (v2.1)
- ✅ Portfolio Management System
- ✅ Data Export (CSV/ZIP)
- ✅ Dark/Light Themes
- ✅ Stock Market Integration (Global + Russian)
- ✅ CS2 Market Integration
- ✅ ~2,750 lines of production code

### Already Implemented from Original Spec
From the 10 requested features, **4 are already complete**:
- ✅ 3.1 Stock Support (Global & Russian stocks via yfinance + MOEX)
- ✅ 3.2 Portfolio Tracker (Multi-asset with real-time valuation)
- ✅ 3.3 CS2 Items (30+ items, multi-marketplace comparison)
- ✅ 3.9 Dark/Light Themes (Settings integration, persistent preference)

### Remaining Features (6)
- 🔜 3.4 Crypto News Notifications (v2.2)
- 🔜 3.5 Weekly Analytics Reports (v2.2)
- 🔜 3.10 Forecast Model Comparison (v2.2)
- 🔜 3.8 Google Sheets/Notion Integration (v2.3)
- 🔜 3.7 Voice Input (v2.4)
- 🔜 3.6 Web Dashboard (v2.4)

---

## 🎯 Version Release Plan

| Version | Features | Timeline | Effort | Priority |
|---------|----------|----------|--------|----------|
| **v2.2** | News, Analytics, Forecast Comparison | Nov-Dec 2025 | 3-4 weeks | High |
| **v2.3** | Google Sheets, Notion, Advanced Export | Jan-Feb 2026 | 3-4 weeks | Medium |
| **v2.4** | Voice Input, Web Dashboard | Mar-Apr 2026 | 4-6 weeks | Medium |
| **v2.5** | NFT Support, DeFi Integration | Jul-Sep 2026 | 6-8 weeks | Low |

---

## 📦 v2.2: News & Analytics (November-December 2025)

### Overview
Focus on information delivery and forecast accuracy. Highest user value with moderate implementation complexity.

### Feature 1: Crypto News Notifications 📰

**Business Value:** HIGH - Keep users informed about market events

#### Technical Design

**Service Layer: `services/news_service.py`**
```python
class NewsService:
    def __init__(self, db, cache_ttl=300):
        self.feeds = {
            'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'cointelegraph': 'https://cointelegraph.com/rss',
            'cryptoslate': 'https://cryptoslate.com/feed/'
        }
        
    async def fetch_news(self, sources: List[str]) -> List[NewsItem]
    async def filter_by_asset(self, news: List[NewsItem], asset: str) -> List[NewsItem]
    async def get_latest_news(self, user_id: int) -> List[NewsItem]
    def check_subscriptions(self) -> None  # Called by APScheduler
```

**Database Schema:**
```python
class NewsSubscription(Base):
    __tablename__ = 'news_subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    asset_symbol = Column(String(10))
    frequency = Column(String(20))  # 'realtime', 'hourly', 'daily'
    categories = Column(JSON)  # ['updates', 'hacks', 'listings']
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Handler: `handlers/news_handler.py`**
- News menu button → Show subscribed assets
- Subscribe/unsubscribe UI
- News feed view (latest 10 items)
- Category filtering

**Localization:**
- 20+ new strings (EN/RU)
- News categories, subscription messages

**Dependencies:**
- `feedparser` ^6.0 (RSS parsing)
- Existing APScheduler integration

**Implementation Steps:**
1. Create `NewsService` with RSS parsing (2 days)
2. Add database model and repository methods (1 day)
3. Create `NewsHandler` with subscription UI (2 days)
4. Integrate APScheduler task (1 day)
5. Add localization strings (0.5 day)
6. Testing and refinement (1 day)

**Total Estimate:** 7.5 days

---

### Feature 2: Weekly Analytics Reports 📊

**Business Value:** MEDIUM - Passive information delivery

#### Technical Design

**Service Layer: `services/report_service.py`**
```python
class ReportService:
    def __init__(self, db, chart_generator, portfolio_service):
        pass
        
    async def generate_weekly_digest(self, user_id: int) -> ReportData
    async def generate_monthly_digest(self, user_id: int) -> ReportData
    async def create_report_image(self, data: ReportData) -> bytes
    def schedule_reports(self) -> None  # APScheduler
```

**Report Content:**
- Portfolio performance (7/30 day change)
- Best/worst performing assets
- Market trend summary
- Top gainers/losers across tracked assets
- Visual: Bar chart with performance

**Database Schema:**
```python
class ReportSubscription(Base):
    __tablename__ = 'report_subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    frequency = Column(String(20))  # 'weekly', 'monthly'
    delivery_day = Column(Integer)  # 1-7 for weekly, 1-31 for monthly
    enabled = Column(Boolean, default=True)
```

**Handler: `handlers/report_handler.py`**
- Report menu (view latest, configure subscription)
- Generate on-demand report
- Schedule configuration

**Implementation Steps:**
1. Create `ReportService` with data aggregation (2 days)
2. Implement report visualization (2 days)
3. Add database model (0.5 day)
4. Create handler UI (1.5 days)
5. Integrate scheduling (1 day)
6. Testing (1 day)

**Total Estimate:** 8 days

---

### Feature 3: Forecast Model Comparison 🎯

**Business Value:** MEDIUM - Builds trust in predictions

#### Technical Design

**Service Enhancement: `services/prediction.py`**
```python
class PredictionGenerator:
    # Existing methods...
    
    async def track_prediction_accuracy(self, prediction_id: int, actual_price: float)
    async def calculate_model_metrics(self, asset: str, days: int) -> Dict
    async def get_best_model(self, asset: str) -> str
```

**Database Schema:**
```python
class PredictionHistory(Base):
    __tablename__ = 'prediction_history'
    
    id = Column(Integer, primary_key=True)
    asset_symbol = Column(String(10))
    model_type = Column(String(20))  # 'arima', 'linreg'
    predicted_price = Column(Float)
    actual_price = Column(Float)
    prediction_date = Column(DateTime)
    target_date = Column(DateTime)
    mae = Column(Float)
    mse = Column(Float)
```

**Implementation:**
- Store predictions when generated
- Daily job to compare with actual prices
- Calculate MAE/MSE metrics
- Display in stats menu
- Auto-select best model per asset

**Implementation Steps:**
1. Extend database schema (1 day)
2. Add tracking to prediction service (2 days)
3. Create comparison job (1 day)
4. Update stats handler to show accuracy (1 day)
5. Testing (1 day)

**Total Estimate:** 6 days

---

### v2.2 Summary

**Total Development Time:** 21.5 days (~4.5 weeks)  
**Testing & QA:** 1 week  
**Documentation:** 0.5 week  
**Total:** ~6 weeks (Nov-Dec 2025)

**Deliverables:**
- News notification system with 3 RSS feeds
- Weekly/monthly automated reports
- Prediction accuracy tracking and display
- 40+ new localization strings
- Updated documentation

---

## 📦 v2.3: Integration & Export (January-February 2026)

### Feature 1: Google Sheets Integration 📤

**Business Value:** HIGH - Requested by power users

#### Technical Design

**Service: `services/sheets_service.py`**
```python
class GoogleSheetsService:
    def __init__(self, db):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        
    async def authenticate_user(self, user_id: int, auth_code: str) -> bool
    async def export_portfolio(self, user_id: int, sheet_id: str)
    async def export_alerts(self, user_id: int, sheet_id: str)
    async def export_history(self, user_id: int, sheet_id: str)
    async def create_sheet(self, user_id: int, name: str) -> str
```

**OAuth Flow:**
1. User clicks "Connect Google Sheets"
2. Bot provides OAuth URL
3. User authorizes on Google
4. Callback receives auth code
5. Exchange for access/refresh tokens
6. Store encrypted tokens in DB

**Database Schema:**
```python
class ExportConfiguration(Base):
    __tablename__ = 'export_configurations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    service = Column(String(20))  # 'google_sheets', 'notion'
    credentials = Column(LargeBinary)  # Encrypted
    target_id = Column(String(200))  # Sheet ID or Notion page
    auto_sync = Column(Boolean, default=False)
    sync_frequency = Column(String(20))  # 'daily', 'weekly'
```

**Dependencies:**
- `google-auth` ^2.23
- `google-auth-oauthlib` ^1.1
- `google-api-python-client` ^2.100

**Implementation Steps:**
1. Set up Google Cloud project and OAuth (1 day)
2. Create `SheetsService` with auth flow (3 days)
3. Implement export methods (2 days)
4. Add database schema (0.5 day)
5. Create handler UI (2 days)
6. Add scheduling for auto-sync (1 day)
7. Testing (1.5 days)

**Total Estimate:** 11 days

---

### Feature 2: Notion Integration 📝

**Business Value:** MEDIUM - Growing platform

#### Technical Design

**Service: `services/notion_service.py`**
```python
class NotionService:
    def __init__(self, db):
        self.api_url = 'https://api.notion.com/v1'
        
    async def authenticate_user(self, user_id: int, api_key: str) -> bool
    async def export_to_database(self, user_id: int, database_id: str, data_type: str)
    async def create_portfolio_page(self, user_id: int) -> str
```

**Implementation:** Similar to Sheets but simpler (API key based auth)

**Implementation Steps:**
1. Create `NotionService` (2 days)
2. Implement export methods (2 days)
3. Handler UI (1 day)
4. Testing (1 day)

**Total Estimate:** 6 days

---

### v2.3 Summary

**Total Development Time:** 17 days (~3.5 weeks)  
**Testing & QA:** 1 week  
**Total:** ~4.5 weeks (Jan-Feb 2026)

---

## 📦 v2.4: Voice & Web (March-April 2026)

### Feature 1: Voice Input Support 🎤

**Business Value:** MEDIUM - UX enhancement

#### Technical Design

**Service: `services/speech_service.py`**
```python
class SpeechRecognitionService:
    def __init__(self):
        # OpenAI Whisper or Yandex SpeechKit
        
    async def transcribe_voice(self, audio_file: bytes, lang: str) -> str
    async def parse_conversion_request(self, text: str) -> Dict
```

**Handler:** Voice message handler in bot
- Download voice message
- Convert to proper format (OGG → WAV)
- Send to speech service
- Parse result as conversion request
- Execute and respond

**Dependencies:**
- `openai` ^1.0 (for Whisper API)
- `pydub` ^0.25 (audio conversion)

**Implementation Steps:**
1. Create `SpeechService` (2 days)
2. Add voice message handler (2 days)
3. Integrate with existing conversion logic (1 day)
4. Add settings toggle (0.5 day)
5. Testing (1.5 days)

**Total Estimate:** 7 days

---

### Feature 2: Web Dashboard (Mini App) 🌐

**Business Value:** HIGH - Future-proof platform

#### Technical Design

**Architecture:**
```
webapp/
├── backend/
│   ├── api/
│   │   ├── auth.py       # Telegram Web App auth
│   │   ├── portfolio.py  # Portfolio endpoints
│   │   ├── alerts.py     # Alert management
│   │   └── charts.py     # Chart generation
│   ├── main.py           # FastAPI app
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/   # Vue/React components
    │   ├── views/        # Page views
    │   └── api/          # API client
    ├── public/
    └── package.json
```

**Backend (FastAPI):**
```python
@app.get("/api/portfolio")
async def get_portfolio(user_id: int = Depends(verify_telegram_auth)):
    # Return portfolio data
    
@app.post("/api/portfolio/add")
async def add_asset(asset: AssetCreate, user_id: int = Depends(...)):
    # Add asset to portfolio
```

**Frontend (Vue.js):**
- Dashboard with portfolio overview
- Chart visualization (Chart.js)
- Alert management
- Export controls
- Settings panel

**Telegram Integration:**
```python
# Bot button
InlineKeyboardButton("🌐 Open Dashboard", web_app=WebAppInfo(url="https://webapp.url"))
```

**Dependencies:**
- Backend: `fastapi` ^0.104, `uvicorn` ^0.24
- Frontend: `vue` ^3.3, `chart.js` ^4.4, `axios` ^1.5

**Implementation Steps:**
1. Set up FastAPI backend (2 days)
2. Implement auth with Telegram (2 days)
3. Create API endpoints (3 days)
4. Build frontend UI (5 days)
5. Integrate with bot (1 day)
6. Deployment setup (2 days)
7. Testing (2 days)

**Total Estimate:** 17 days

---

### v2.4 Summary

**Total Development Time:** 24 days (~5 weeks)  
**Testing & QA:** 1.5 weeks  
**Total:** ~6.5 weeks (Mar-Apr 2026)

---

## 📊 Resource Requirements

### Development Team
- **Backend Developer:** 1 FTE
- **Frontend Developer (for Web Dashboard):** 0.5 FTE
- **QA Engineer:** 0.3 FTE
- **DevOps (for Web Dashboard):** 0.2 FTE

### Infrastructure
- **Current:** VPS/Docker sufficient
- **v2.4+:** Additional server for Web Dashboard
- **Cost Estimate:** +$20-30/month for web hosting

### External Services
- Google Cloud (Sheets API): Free tier sufficient
- OpenAI (Whisper API): ~$0.006/minute
- Notion API: Free
- RSS Feeds: Free

---

## 🧪 Testing Strategy

### Unit Tests
- All new services must have 80%+ coverage
- Mock external APIs (Google, Notion, OpenAI)

### Integration Tests
- End-to-end user flows
- Database operations
- API integrations

### User Acceptance Testing
- Beta group (10-20 users)
- Feature feedback collection
- Bug reporting via GitHub Issues

---

## 📝 Documentation Updates

Each version requires:
- README.md updates
- CHANGELOG.md entries
- API documentation (for v2.4 webapp)
- User guides (in docs/)
- Inline code comments

---

## 🚀 Deployment Strategy

### Continuous Deployment
- GitHub Actions CI/CD
- Automated tests on PR
- Staging environment testing
- Production deployment on merge to main

### Database Migrations
- Alembic migration scripts
- Backward compatibility
- Rollback procedures

### Rollout Plan
- v2.2: Direct deployment (news/reports are additive)
- v2.3: Phased rollout (OAuth needs careful testing)
- v2.4: Beta testing required (new platform)

---

## ⚠️ Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| API rate limits | Medium | Medium | Caching, user limits |
| OAuth complexity | High | Low | Thorough testing, docs |
| Voice recognition accuracy | Medium | Medium | Multiple providers, fallback |
| Web dashboard security | High | Low | Proper auth, HTTPS only |
| External service outages | Medium | Medium | Graceful degradation |

---

## 📈 Success Metrics

### v2.2 (News & Analytics)
- 30%+ users subscribe to news
- 50%+ users view at least one report
- Prediction accuracy improves by 10%

### v2.3 (Integration)
- 20%+ users export to Sheets/Notion
- 100+ active exports per week

### v2.4 (Voice & Web)
- 15%+ users try voice input
- 25%+ users access web dashboard
- Dashboard DAU >10% of bot users

---

## 🎯 Post-v2.4 Planning

### v2.5 Candidates
- NFT marketplace integration
- DeFi protocol tracking
- Social features (leaderboards)
- Trading signals
- Premium tier

### Long-term Vision (v3.0)
- Multi-chain support
- Advanced AI (GPT-4 integration)
- Mobile app (Flutter)
- API for developers
- White-label solution

---

**Document Status:** DRAFT  
**Next Review:** November 1, 2025  
**Approved By:** Pending

---

*This plan is subject to change based on user feedback, technical discoveries, and resource availability.*
