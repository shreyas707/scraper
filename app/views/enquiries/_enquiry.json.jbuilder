json.extract! enquiry, :id, :title, :name, :date, :status, :location_preference, :link, :area_id, :category_id, :created_at, :updated_at
json.url enquiry_url(enquiry, format: :json)
