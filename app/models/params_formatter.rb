class ParamsFormatter
	
	def initialize params
		@params = params
		@category_name = params[:category]
		@area_name = params[:area]
		@city_name = params[:city]
		@city = City.where(name: @city_name) 
		@area = Area.find_by_name(@area_name)
		@category = Category.find_by_name(@category_name)
		# binding.pry
	end

	def generate
		data = {area_id: generate_city_area , category_id: generate_category }
		data
		# binding.pry
	end

	def generate_city_area
		if @city.present? && @area.nil?
			@area = Area.create(name: @area_name, city_id: @city.first.id)
		else
			if @city.present? 
				@area = Area.create(name: @area_name, city_id: @city.first.id) if @area.nil?
			else
				city = City.create(name: @city_name)
				@area = Area.create(name: @area_name, city_id: city.id) 
			end
		end
		@area.id
	end

	def generate_category
		# binding.pry
		@category = Category.create(name: @category_name) if @category.nil?
		# binding.pry
		@category.id
	end

end