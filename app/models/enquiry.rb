class Enquiry < ActiveRecord::Base

	belongs_to :area
	belongs_to :category

	validates_presence_of :title, :name, :status, :location_preference, :link#, :area_id, :category_id, :date

end