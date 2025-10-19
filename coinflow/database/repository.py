"""Database repository for CoinFlow bot."""

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple
from .models import Base, User, Alert, ConversionHistory, Favorite, PortfolioItem


class DatabaseRepository:
    """Repository for database operations."""
    
    def __init__(self, database_url: str):
        """Initialize database connection."""
        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
    
    def get_session(self):
        """Get a database session."""
        return self.Session()
    
    # --- User operations ---
    
    def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.telegram_id == telegram_id).first()
        finally:
            session.close()
    
    def create_user(self, telegram_id: int, lang: str = 'en') -> User:
        """Create a new user."""
        session = self.get_session()
        try:
            user = User(
                telegram_id=telegram_id,
                lang=lang,
                providers={}
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def get_or_create_user(self, telegram_id: int, lang: str = 'en') -> User:
        """Get existing user or create new one."""
        user = self.get_user(telegram_id)
        if not user:
            user = self.create_user(telegram_id, lang)
        return user
    
    def update_user(self, telegram_id: int, **kwargs) -> Optional[User]:
        """Update user settings."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.updated_at = datetime.utcnow()
                session.commit()
                session.refresh(user)
            return user
        finally:
            session.close()
    
    # --- Alert operations ---
    
    def add_alert(self, user_id: int, pair: str, condition: str, target: float) -> Alert:
        """Add a new alert."""
        session = self.get_session()
        try:
            alert = Alert(
                user_id=user_id,
                pair=pair.upper(),
                condition=condition,
                target=target
            )
            session.add(alert)
            session.commit()
            session.refresh(alert)
            return alert
        finally:
            session.close()
    
    def get_alerts(self, user_id: int) -> List[Alert]:
        """Get all alerts for a user."""
        session = self.get_session()
        try:
            return session.query(Alert).filter(Alert.user_id == user_id).all()
        finally:
            session.close()
    
    def get_all_alerts(self) -> List[Alert]:
        """Get all alerts from all users."""
        session = self.get_session()
        try:
            return session.query(Alert).all()
        finally:
            session.close()
    
    def remove_alert(self, alert_id: int):
        """Remove an alert."""
        session = self.get_session()
        try:
            alert = session.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                session.delete(alert)
                session.commit()
        finally:
            session.close()
    
    def remove_alerts(self, alert_ids: List[int]):
        """Remove multiple alerts."""
        session = self.get_session()
        try:
            session.query(Alert).filter(Alert.id.in_(alert_ids)).delete(synchronize_session=False)
            session.commit()
        finally:
            session.close()
    
    # --- Conversion history operations ---
    
    def add_conversion(self, user_id: int, from_currency: str, to_currency: str,
                      amount: float, result: float, rate: float) -> ConversionHistory:
        """Add a conversion to history."""
        session = self.get_session()
        try:
            conversion = ConversionHistory(
                user_id=user_id,
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                result=result,
                rate=rate
            )
            session.add(conversion)
            session.commit()
            session.refresh(conversion)
            return conversion
        finally:
            session.close()
    
    def get_conversion_history(self, user_id: int, limit: int = 10) -> List[ConversionHistory]:
        """Get conversion history for a user."""
        session = self.get_session()
        try:
            return session.query(ConversionHistory)\
                .filter(ConversionHistory.user_id == user_id)\
                .order_by(desc(ConversionHistory.timestamp))\
                .limit(limit)\
                .all()
        finally:
            session.close()
    
    def get_popular_pairs(self, user_id: int, days: int = 30, limit: int = 5) -> List[tuple]:
        """Get most popular conversion pairs for a user."""
        session = self.get_session()
        try:
            since = datetime.utcnow() - timedelta(days=days)
            results = session.query(
                ConversionHistory.from_currency,
                ConversionHistory.to_currency,
                func.count().label('count')
            ).filter(
                ConversionHistory.user_id == user_id,
                ConversionHistory.timestamp >= since
            ).group_by(
                ConversionHistory.from_currency,
                ConversionHistory.to_currency
            ).order_by(desc('count')).limit(limit).all()
            
            return [(r[0], r[1], r[2]) for r in results]
        finally:
            session.close()
    
    # --- Favorite operations ---
    
    def add_favorite(self, user_id: int, currency: str) -> Favorite:
        """Add a currency to favorites."""
        session = self.get_session()
        try:
            # Check if already exists
            existing = session.query(Favorite).filter(
                Favorite.user_id == user_id,
                Favorite.currency == currency.upper()
            ).first()
            
            if existing:
                return existing
            
            favorite = Favorite(
                user_id=user_id,
                currency=currency.upper()
            )
            session.add(favorite)
            session.commit()
            session.refresh(favorite)
            return favorite
        finally:
            session.close()
    
    def remove_favorite(self, user_id: int, currency: str):
        """Remove a currency from favorites."""
        session = self.get_session()
        try:
            session.query(Favorite).filter(
                Favorite.user_id == user_id,
                Favorite.currency == currency.upper()
            ).delete()
            session.commit()
        finally:
            session.close()
    
    def get_favorites(self, user_id: int) -> List[str]:
        """Get all favorite currencies for a user."""
        session = self.get_session()
        try:
            favorites = session.query(Favorite).filter(Favorite.user_id == user_id).all()
            return [f.currency for f in favorites]
        finally:
            session.close()
    
    def is_favorite(self, user_id: int, currency: str) -> bool:
        """Check if a currency is in favorites."""
        session = self.get_session()
        try:
            return session.query(Favorite).filter(
                Favorite.user_id == user_id,
                Favorite.currency == currency.upper()
            ).first() is not None
        finally:
            session.close()
    
    # --- Statistics ---
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get statistics for a user."""
        session = self.get_session()
        try:
            total_conversions = session.query(ConversionHistory).filter(
                ConversionHistory.user_id == user_id
            ).count()
            
            total_alerts = session.query(Alert).filter(
                Alert.user_id == user_id
            ).count()
            
            favorites_count = session.query(Favorite).filter(
                Favorite.user_id == user_id
            ).count()
            
            return {
                'total_conversions': total_conversions,
                'total_alerts': total_alerts,
                'favorites_count': favorites_count
            }
        finally:
            session.close()
    
    # --- Portfolio operations ---
    
    def add_portfolio_item(self, user_id: int, asset_type: str, asset_symbol: str, 
                          asset_name: str, quantity: float, purchase_price: float = None,
                          purchase_date: datetime = None, notes: str = None) -> PortfolioItem:
        """Add a new item to user's portfolio."""
        session = self.get_session()
        try:
            item = PortfolioItem(
                user_id=user_id,
                asset_type=asset_type,
                asset_symbol=asset_symbol.upper(),
                asset_name=asset_name,
                quantity=quantity,
                purchase_price=purchase_price,
                purchase_date=purchase_date,
                notes=notes
            )
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
        finally:
            session.close()
    
    def get_portfolio_items(self, user_id: int, asset_type: str = None) -> List[PortfolioItem]:
        """Get all portfolio items for a user, optionally filtered by asset type."""
        session = self.get_session()
        try:
            query = session.query(PortfolioItem).filter(PortfolioItem.user_id == user_id)
            if asset_type:
                query = query.filter(PortfolioItem.asset_type == asset_type)
            return query.order_by(PortfolioItem.created_at.desc()).all()
        finally:
            session.close()
    
    def get_portfolio_item(self, item_id: int, user_id: int) -> Optional[PortfolioItem]:
        """Get a specific portfolio item."""
        session = self.get_session()
        try:
            return session.query(PortfolioItem).filter(
                PortfolioItem.id == item_id,
                PortfolioItem.user_id == user_id
            ).first()
        finally:
            session.close()
    
    def update_portfolio_item(self, item_id: int, user_id: int, **kwargs) -> Optional[PortfolioItem]:
        """Update a portfolio item."""
        session = self.get_session()
        try:
            item = session.query(PortfolioItem).filter(
                PortfolioItem.id == item_id,
                PortfolioItem.user_id == user_id
            ).first()
            if item:
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                item.updated_at = datetime.utcnow()
                session.commit()
                session.refresh(item)
            return item
        finally:
            session.close()
    
    def delete_portfolio_item(self, item_id: int, user_id: int) -> bool:
        """Delete a portfolio item."""
        session = self.get_session()
        try:
            deleted = session.query(PortfolioItem).filter(
                PortfolioItem.id == item_id,
                PortfolioItem.user_id == user_id
            ).delete()
            session.commit()
            return deleted > 0
        finally:
            session.close()
    
    def get_portfolio_summary(self, user_id: int) -> Dict:
        """Get summary statistics for user's portfolio."""
        session = self.get_session()
        try:
            items = session.query(PortfolioItem).filter(PortfolioItem.user_id == user_id).all()
            
            # Count by type
            type_counts = {}
            for item in items:
                type_counts[item.asset_type] = type_counts.get(item.asset_type, 0) + 1
            
            return {
                'total_items': len(items),
                'by_type': type_counts,
                'last_updated': max([item.updated_at for item in items]).isoformat() if items else None
            }
        finally:
            session.close()
