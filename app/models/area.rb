class Area < ActiveRecord::Base

	has_many :enquiries

	belongs_to :city

	validates_uniqueness_of :name
	validates_presence_of :name#, :city_id

end