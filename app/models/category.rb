class Category < ActiveRecord::Base

	has_many :enquiry

	validates_uniqueness_of :name
	validates_presence_of :name

end

