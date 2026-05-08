"""
Complete Workflow: Ingest → Process → Upload
One script to do everything
"""

import sys
import time
from datetime import datetime
from pipelines.ingestion_pipeline import IngestionPipeline
from pipelines.processing_pipeline import ProcessingPipeline
from services.database_service import get_database_service
from services.firebase_service import get_firebase_service
from core.logger import get_logger
from core.constants import FIREBASE_MEDICINES_PATH

logger = get_logger(__name__)

def print_header(step, title):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"STEP {step}: {title}")
    print(f"{'='*70}\n")

def step_1_ingest():
    """Step 1: Ingest data"""
    print_header(1, "DATA INGESTION")
    
    try:
        print("📍 Ingesting data from CSV...")
        pipeline = IngestionPipeline()
        success = pipeline.ingest_data('data/raw/medicine_inventory.csv')
        
        if success:
            print("✅ Ingestion successful\n")
            return True
        else:
            print("❌ Ingestion failed\n")
            return False
    
    except Exception as e:
        logger.error(f"Ingestion error: {str(e)}")
        print(f"❌ Ingestion error: {str(e)}\n")
        return False

def step_2_process():
    """Step 2: Process data"""
    print_header(2, "DATA PROCESSING")
    
    try:
        print("📍 Processing data...")
        
        # Load data
        db = get_database_service()
        df = db.load_medicine_data('data/raw/medicine_inventory.csv')
        
        if df is None:
            print("❌ Failed to load data\n")
            return False, None
        
        print(f"✅ Loaded {len(df)} records")
        
        # Process
        pipeline = ProcessingPipeline()
        processed = pipeline.process_data(df)
        
        print(f"✅ Processing successful")
        print(f"   • Original columns: {len(df.columns)}")
        print(f"   • Processed columns: {len(processed.columns)}")
        print(f"   • Records: {len(processed)}\n")
        
        return True, processed
    
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        print(f"❌ Processing error: {str(e)}\n")
        return False, None

def step_3_upload(processed_df):
    """Step 3: Upload to Firebase"""
    print_header(3, "UPLOAD TO FIREBASE")
    
    try:
        print("📍 Initializing Firebase...")
        firebase = get_firebase_service()
        
        if not firebase.check_connection():
            print("❌ Firebase connection failed\n")
            return False
        
        print("✅ Firebase connected")
        
        print(f"\n📍 Preparing {len(processed_df)} records for upload...")
        
        # Prepare data
        firebase_data = {}
        for index, row in processed_df.iterrows():
            medicine_id = row.get('medicine_id', index)
            medicine_data = row.to_dict()
            firebase_data[f"medicine_{medicine_id}"] = medicine_data
        
        print(f"✅ Prepared {len(firebase_data)} records")
        
        # Upload
        print(f"\n📍 Uploading to Firebase...")
        batch_data = {f"{FIREBASE_MEDICINES_PATH}/{key}": value for key, value in firebase_data.items()}
        
        success = firebase.batch_write(batch_data)
        
        if success:
            print(f"✅ Upload successful")
            print(f"   • Total records: {len(firebase_data)}")
            print(f"   • Firebase path: {FIREBASE_MEDICINES_PATH}\n")
            return True
        else:
            print("❌ Upload failed\n")
            return False
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        print(f"❌ Upload error: {str(e)}\n")
        return False

def step_4_verify():
    """Step 4: Verify upload"""
    print_header(4, "VERIFICATION")
    
    try:
        print("📍 Verifying Firebase data...")
        firebase = get_firebase_service()
        data = firebase.get_data('/medicines')
        
        if data and isinstance(data, dict):
            count = len(data)
            print(f"✅ Verification successful")
            print(f"   • Records in Firebase: {count}")
            print(f"   • Sample records:")
            
            for i, (key, val) in enumerate(list(data.items())[:3]):
                med_name = val.get('medicine_name', 'Unknown') if isinstance(val, dict) else 'N/A'
                print(f"     {i+1}. {key}: {med_name}")
            
            print()
            return True
        else:
            print("❌ Verification failed - No data in Firebase\n")
            return False
    
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        print(f"❌ Verification error: {str(e)}\n")
        return False

def main():
    """Run complete workflow"""
    print("\n" + "="*70)
    print("🔄 COMPLETE WORKFLOW: INGEST → PROCESS → UPLOAD")
    print("="*70)
    print(f"\nStart Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = time.time()
    
    # Step 1: Ingest
    if not step_1_ingest():
        print("❌ Workflow failed at ingestion step")
        return False
    
    time.sleep(1)
    
    # Step 2: Process
    success, processed_df = step_2_process()
    if not success:
        print("❌ Workflow failed at processing step")
        return False
    
    time.sleep(1)
    
    # Step 3: Upload
    if not step_3_upload(processed_df):
        print("❌ Workflow failed at upload step")
        return False
    
    time.sleep(1)
    
    # Step 4: Verify
    if not step_4_verify():
        print("⚠️  Workflow completed but verification failed")
        return False
    
    # Summary
    elapsed = time.time() - start_time
    
    print("="*70)
    print("✅ COMPLETE WORKFLOW SUCCESSFUL")
    print("="*70)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Duration: {elapsed:.2f} seconds\n")
    
    print("📊 What's Next?")
    print("   1. Launch dashboard: streamlit run main.py")
    print("   2. Start simulator: python scripts/simulate_updates.py")
    print("   3. Monitor changes: python monitor_realtime.py")
    print()
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
