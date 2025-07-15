import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1 import query, aggregation
import threading

class FireBaseService:
    def __init__(self, cred):
        self.cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.callback_done = threading.Event()

    def list_collections(self):
        """取得所有 collection 名稱"""
        return [c.id for c in self.db.collections()]

    def get_collection_data(self, collection):
        """取得集合所有資料"""
        docs = self.db.collection(collection).stream()
        return [{'_id': doc.id, **doc.to_dict()} for doc in docs]

    def get_data(self, collection, doc_id):
        """取得資料"""
        doc_ref = self.db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        return doc.to_dict()
    
    def filter_data(self, collection, conditions, order_by=None, limit=None):
        """篩選資料\n
        conditions format:
        [
          ("field", "operator", "value"),
          ...
        ]
        
        Example: [("age", ">", 20)]

        order_by format:
        ("field", "direction")
        direction: "asc" or "desc" (default: "asc")
        Example: ("age", "desc")
        """
        collection_ref = self.db.collection(collection)
        for condition in conditions:
            collection_ref = collection_ref.where(filter=FieldFilter(*condition))
        if order_by:
            field = order_by[0]
            direction = query.Query.DESCENDING if order_by[1] == 'desc' else query.Query.ASCENDING
            collection_ref = collection_ref.order_by(field, direction=direction)
        if limit:
            collection_ref = collection_ref.limit(limit)
        docs = collection_ref.stream()
        return [{'_id': doc.id, **doc.to_dict()} for doc in docs]
    
    def get_aggregate_count(self, collection, conditions):
        """
        取得collection經過條件篩選後的總筆數
        """
        collection_ref = self.db.collection(collection)
        for condition in conditions:
            collection_ref = collection_ref.where(filter=FieldFilter(*condition))
        aggregate_query = aggregation.AggregationQuery(collection_ref)
        aggregate_query.count()
        results = aggregate_query.get()

        return results[0][0].value
    
    def add_data(self, collection, doc_id, data):
        """新增資料"""
        doc_ref = self.db.collection(collection).document(doc_id)
        doc_ref.set(data)

    def update_data(self, collection, doc_id, data):
        """更新資料"""
        doc_ref = self.db.collection(collection).document(doc_id)
        doc_ref.update(data)

    def delete_data(self, collection, doc_id):
        """刪除資料"""
        doc_ref = self.db.collection(collection).document(doc_id)
        doc_ref.delete()

    def on_snapshot(self, collection):
        """監聽文件變更"""
        def callback(doc_snapshot, changes, read_time):
            for change in changes:
                # 檢測變更類型
                if change.type.name == 'MODIFIED':
                    print(f"Document modified: {change.document.id}")
                    self.update_correct_rate(change.document)

        # 監聽集合
        doc_ref = self.db.collection(collection)
        doc_watch = doc_ref.on_snapshot(callback)
        return doc_watch
